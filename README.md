# UberScrape

**AI-powered web scraping that returns structured data, not HTML walls.**

Turn any website into clean, structured JSON/CSV using Claude AI for intelligent extraction.

## What It Does

- **Search** → Brave Search API with structured results
- **Extract** → Fetch any URL, get structured JSON (not raw HTML)
- **Map** → Discover all URLs on a site
- **Crawl** → Bulk extract from entire websites

## Why UberScrape?

**Traditional scrapers:**
```python
# Brittle CSS selectors that break on layout changes
price = soup.select('.price-container > span.amount')[0].text
```

**UberScrape:**
```python
# AI understands the page, extracts what you ask for
result = await scraper.extract(url, schema={
    "price": "number",
    "title": "string",
    "sqft": "number"
})
# Returns: {"price": 1500, "title": "2BR Apartment", "sqft": 850}
```

## Quick Start

### Installation

```bash
pip install uberscrape
```

### Extract from a URL

```bash
uberscrape extract \
  --url "https://example.com/listing" \
  --schema schemas/rental-listing.json \
  --output results.json
```

### Batch Processing

```bash
# Extract from multiple URLs in parallel
uberscrape extract \
  --urls urls.txt \
  --schema schemas/product.json \
  --parallel 5 \
  --output results.csv
```

### Search + Extract

```bash
# Search web, then extract from results
uberscrape search "2BR rentals Phoenix" \
  --extract \
  --limit 10 \
  --schema schemas/rental-listing.json
```

## Features

✅ **LLM-Powered Extraction** — Claude AI parses pages intelligently  
✅ **Parallel Processing** — Scrape 10+ pages simultaneously  
✅ **JavaScript Rendering** — Handles dynamic sites (Playwright)  
✅ **Structured Output** — JSON, CSV, or Markdown tables  
✅ **Preview Mode** — Review data before export  
✅ **Error Handling** — Graceful degradation (1 failure ≠ batch failure)  
✅ **Deduplication** — Fuzzy matching to remove duplicates  
✅ **Normalization** — Clean prices, dates, phone numbers  

## Use Cases

- **Real Estate:** Extract rental listings, property details
- **E-commerce:** Product data, prices, reviews
- **Research:** Academic papers, news articles
- **Lead Generation:** Business directories, contact info
- **Monitoring:** Price tracking, content changes
- **Documentation:** Crawl entire docs sites

## Architecture

```
URL → Fetch (httpx/Playwright) → HTML → Markdown (html2text)
                                            ↓
                            Claude API with schema → Structured JSON
                                            ↓
                            Normalize → Dedupe → Export (JSON/CSV)
```

## Security

- API keys stored in `.env` (gitignored)
- Server-side only (never expose keys to client)
- Respects robots.txt
- Rate limiting built-in

## Tech Stack

- **Python 3.9+** — Core runtime
- **httpx** — Fast async HTTP
- **Playwright** — JavaScript rendering
- **Claude (Anthropic)** — AI extraction
- **html2text** — Clean markdown conversion
- **Click** — Professional CLI
- **Rich** — Beautiful terminal output

## Development

Built for [VibeCodersToolbox](https://vibecoderstoolbox.com)

---

**License:** MIT  
**Author:** Doug Simpson  
**Created:** 2026-02-25
