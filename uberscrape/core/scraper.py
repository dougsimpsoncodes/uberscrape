"""
Core scraper class - handles fetching, parsing, and extraction
"""

import asyncio
import httpx
from typing import List, Dict, Optional, Any
from playwright.async_api import async_playwright, Browser, Page
import html2text
from anthropic import AsyncAnthropic
import json
from json_repair import repair_json

class WebScraper:
    """
    AI-powered web scraper that returns structured data instead of HTML.
    
    Uses Claude AI to intelligently extract data from web pages based on
    user-defined schemas.
    """
    
    def __init__(
        self,
        anthropic_key: str,
        brave_key: Optional[str] = None,
        use_browser: bool = False,
        timeout: int = 30,
        max_concurrent: int = 5
    ):
        """
        Initialize the scraper.
        
        Args:
            anthropic_key: Claude API key for extraction
            brave_key: Brave Search API key (optional)
            use_browser: Use Playwright for JS rendering (slower but handles dynamic sites)
            timeout: Request timeout in seconds
            max_concurrent: Max parallel requests
        """
        self.client = AsyncAnthropic(api_key=anthropic_key)
        self.brave_key = brave_key
        self.use_browser = use_browser
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # HTML to Markdown converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # Don't wrap lines
        
    async def extract_batch(
        self,
        urls: List[str],
        schema: Dict[str, str],
        parallel: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Extract structured data from multiple URLs in parallel.
        
        Args:
            urls: List of URLs to scrape
            schema: Field definitions {"field_name": "type", ...}
            parallel: Run in parallel (faster) or sequential
            
        Returns:
            List of extracted data dicts (includes errors for failed URLs)
        """
        if parallel:
            tasks = [self._extract_single(url, schema) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Convert exceptions to error dicts
            return [
                result if not isinstance(result, Exception)
                else {"url": urls[i], "error": str(result), "parse_error": True}
                for i, result in enumerate(results)
            ]
        else:
            # Sequential processing
            results = []
            for url in urls:
                try:
                    result = await self._extract_single(url, schema)
                    results.append(result)
                except Exception as e:
                    results.append({"url": url, "error": str(e), "parse_error": True})
            return results
    
    async def _extract_single(
        self,
        url: str,
        schema: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Extract structured data from a single URL.
        
        Args:
            url: URL to scrape
            schema: Field definitions
            
        Returns:
            Extracted data dict or error dict
        """
        async with self.semaphore:  # Rate limiting
            try:
                # Step 1: Fetch HTML
                html = await self._fetch(url)
                
                # Step 2: Convert to markdown (cleaner, fewer tokens)
                markdown = self.h2t.handle(html)
                
                # Trim to reasonable size (Claude context limit)
                if len(markdown) > 50000:
                    markdown = markdown[:50000] + "\n\n[... content truncated ...]"
                
                # Step 3: Extract with Claude
                extracted = await self._extract_with_llm(markdown, schema)
                
                # Step 4: Add metadata
                extracted["url"] = url
                extracted["source"] = "uberscrape"
                
                return extracted
                
            except Exception as e:
                return {
                    "url": url,
                    "error": str(e),
                    "parse_error": True
                }
    
    async def _fetch(self, url: str) -> str:
        """
        Fetch HTML from URL (with or without browser).
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string
        """
        if self.use_browser:
            return await self._fetch_with_browser(url)
        else:
            return await self._fetch_with_httpx(url)
    
    async def _fetch_with_httpx(self, url: str) -> str:
        """Fetch static HTML with httpx (fast)"""
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
            )
            response.raise_for_status()
            return response.text
    
    async def _fetch_with_browser(self, url: str) -> str:
        """Fetch with Playwright (handles JavaScript, slower)"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set realistic user agent
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            })
            
            await page.goto(url, wait_until="networkidle", timeout=self.timeout * 1000)
            
            # Wait a bit for any lazy-loaded content
            await page.wait_for_timeout(2000)
            
            html = await page.content()
            await browser.close()
            
            return html
    
    async def _extract_with_llm(
        self,
        markdown: str,
        schema: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Use Claude to extract structured data from markdown.
        
        Args:
            markdown: Page content as markdown
            schema: Field definitions
            
        Returns:
            Extracted data as dict
        """
        # Build prompt with explicit schema
        prompt = self._build_extraction_prompt(schema, markdown)
        
        # Call Claude API
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0,  # Deterministic for data extraction
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response
        raw_text = response.content[0].text
        
        try:
            # Try parsing as JSON first
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            # Try repairing JSON
            try:
                repaired = repair_json(raw_text)
                data = json.loads(repaired)
            except:
                # Last resort: extract JSON from markdown code block
                import re
                json_match = re.search(r'```json\n(.*?)\n```', raw_text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(1))
                else:
                    # Give up, return error
                    raise ValueError(f"Could not parse LLM response as JSON: {raw_text[:200]}")
        
        return data
    
    def _build_extraction_prompt(
        self,
        schema: Dict[str, str],
        markdown: str
    ) -> str:
        """
        Build the extraction prompt for Claude.
        
        Args:
            schema: Field definitions
            markdown: Page content
            
        Returns:
            Formatted prompt string
        """
        # Convert schema to example JSON
        schema_example = {
            field: f"<{type_}>" for field, type_ in schema.items()
        }
        
        return f"""Extract structured data from this webpage markdown.

Return ONLY valid JSON with this exact structure (no markdown code blocks, no explanation):
{json.dumps(schema_example, indent=2)}

Extraction rules:
- All numbers must be actual numbers (not strings)
- Remove currency symbols ($, €, etc.) from numbers
- Remove commas from numbers (1,500 → 1500)
- Dates should be ISO format (YYYY-MM-DD) if possible
- If a field is not visible on the page, use null
- Phone numbers: keep as strings in original format
- Arrays: extract all matching items found
- Be precise - only extract what's explicitly shown

Webpage content:
{markdown}

Extract the data now:"""

    async def close(self):
        """Cleanup resources"""
        await self.client.close()
