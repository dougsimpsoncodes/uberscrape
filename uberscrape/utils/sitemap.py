"""Sitemap parsing utilities"""

import httpx
import xml.etree.ElementTree as ET
from typing import List, Optional
from urllib.parse import urljoin, urlparse

async def fetch_sitemap_urls(base_url: str, limit: Optional[int] = None) -> List[str]:
    """
    Fetch URLs from a website's sitemap.xml
    
    Args:
        base_url: Base URL of the website
        limit: Maximum number of URLs to return
        
    Returns:
        List of URLs found in sitemap
    """
    urls = []
    
    # Try common sitemap locations
    sitemap_urls = [
        urljoin(base_url, '/sitemap.xml'),
        urljoin(base_url, '/sitemap_index.xml'),
        urljoin(base_url, '/sitemap-index.xml'),
    ]
    
    async with httpx.AsyncClient(timeout=30) as client:
        for sitemap_url in sitemap_urls:
            try:
                response = await client.get(sitemap_url)
                if response.status_code == 200:
                    urls = parse_sitemap_xml(response.text, limit)
                    if urls:
                        return urls
            except:
                continue
    
    return urls

def parse_sitemap_xml(xml_content: str, limit: Optional[int] = None) -> List[str]:
    """Parse URLs from sitemap XML content"""
    urls = []
    
    try:
        root = ET.fromstring(xml_content)
        
        # Handle sitemap index (contains links to other sitemaps)
        if 'sitemapindex' in root.tag:
            # For now, just return empty - could recursively fetch sub-sitemaps
            return []
        
        # Handle regular sitemap
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_elem in root.findall('.//ns:url', namespace):
            loc = url_elem.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text)
                if limit and len(urls) >= limit:
                    break
        
        # Fallback: try without namespace
        if not urls:
            for url_elem in root.findall('.//url'):
                loc = url_elem.find('loc')
                if loc is not None and loc.text:
                    urls.append(loc.text)
                    if limit and len(urls) >= limit:
                        break
    
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
    
    return urls
