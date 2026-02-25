# UberScrape - Project State

## Overview
AI-powered web scraping tool that returns structured data instead of HTML walls. Built for VibeCodersToolbox.

**Status:** 🟡 In Development - Phase 1 MVP  
**Created:** 2026-02-25  
**Last Updated:** 2026-02-25 10:20 MST

---

## Project Goals

### Primary
Build a web-based tool (and CLI) that extracts structured data from websites using AI, not brittle CSS selectors.

### Use Cases
1. Real estate research (rental listings, property data)
2. Competitive analysis (product prices, features)
3. Lead generation (business directories)
4. Documentation scraping (entire doc sites)
5. Price monitoring (e-commerce tracking)

---

## Architecture

### Tech Stack

**Core Python Package:**
- Python 3.9+
- httpx (async HTTP)
- Playwright (JavaScript rendering)
- Claude API (Anthropic) - AI extraction
- html2text - HTML → Markdown conversion
- Click - CLI framework
- Rich - Terminal UI

**Web UI (Phase 2):**
- Next.js 15
- Supabase (database + auth)
- Tailwind CSS
- Vercel deployment

### Data Flow
```
URL → Fetch (httpx or Playwright) 
    → HTML → Markdown (html2text)
    → Claude API + schema
    → Structured JSON
    → Normalize/Dedupe
    → Export (JSON/CSV)
```

---

## Development Phases

### Phase 1: Core Scraper (Current) ✅ IN PROGRESS
**Goal:** Extract from single URL → structured JSON

**Completed:**
- [x] Project structure created
- [x] Core scraper class (`WebScraper`)
- [x] HTTP fetching (httpx)
- [x] Browser rendering (Playwright)
- [x] HTML → Markdown conversion
- [x] Claude API integration
- [x] Schema-based extraction
- [x] Error handling (graceful degradation)
- [x] Example schemas (rental, product)
- [x] GitHub repo initialized

**Next:**
- [ ] CLI implementation (Click)
- [ ] Test on real websites
- [ ] Batch processing
- [ ] Progress indicators
- [ ] Output formats (JSON, CSV, Markdown)

**Timeline:** 2-3 days

### Phase 2: Web UI (Planned)
**Goal:** Web interface for VibeCodersToolbox

**Features:**
- Paste URL or upload URL list
- Select/customize schema
- Preview extracted data
- Export results
- Save to Supabase
- Usage tracking

**Timeline:** 3-4 days

### Phase 3: Advanced Features (Planned)
**Goal:** Production hardening

**Features:**
- Brave Search integration
- Site mapping (discover URLs)
- Bulk crawling
- Caching layer
- Retry logic
- Stealth mode (anti-bot)
- Rate limiting
- Deduplication

**Timeline:** 4-5 days

---

## File Structure

```
uberscrape/
├── uberscrape/               # Python package
│   ├── __init__.py
│   ├── core/
│   │   ├── scraper.py       # Main WebScraper class ✅
│   │   └── extractor.py     # LLM extraction logic
│   ├── utils/
│   │   ├── schema.py        # Schema loading/validation
│   │   ├── normalize.py     # Data normalization
│   │   └── export.py        # Output formatting
│   └── schemas/
│       ├── rental-listing.json  ✅
│       └── product.json         ✅
├── tests/
├── examples/
├── .env.example             ✅
├── .gitignore              ✅
├── README.md               ✅
├── PROJECT-STATE.md        ✅ (this file)
└── pyproject.toml          # Python package config
```

---

## Key Learnings Applied

### From Pink Auto Glass Invoice Parser

1. **Vision API → Structured Data** pattern proven in production
2. **Parallel processing** with per-item error handling
3. **Three-phase architecture** (parse → preview → import)
4. **Normalization layer** for data cleanup
5. **Fuzzy matching** for deduplication
6. **Detailed result reporting** (success/fail/errors)
7. **Schema-first extraction** with explicit types

### Security Best Practices

- API keys in `.env` (gitignored)
- Never expose keys to client
- Server-side extraction only (web UI)
- Validate all inputs
- Rate limiting built-in

---

## API Keys & Configuration

**Required:**
- `ANTHROPIC_API_KEY` - Claude API for extraction

**Optional:**
- `BRAVE_SEARCH_API_KEY` - Web search functionality
- Supabase credentials (for web UI)

**Storage:**
- Local: `.env` file (gitignored)
- Production: Environment variables (Vercel, Railway, etc.)
- DO NOT commit keys to git

---

## Testing Strategy

**Phase 1:**
- Manual testing on real websites
- Known-good sites (docs, listings, products)
- Edge cases (missing fields, malformed HTML)

**Phase 2:**
- Unit tests (pytest)
- Integration tests (real API calls)
- UI testing (Playwright)

**Phase 3:**
- Load testing (parallel scraping)
- Anti-bot detection testing
- Performance benchmarks

---

## Known Limitations

### Current (Phase 1)
- No retry logic (fails on timeout)
- No caching (re-fetches every time)
- No deduplication
- Limited to Claude context window (~50K chars)
- No stealth mode (detectable as bot)

### Future Improvements
- Add retry with exponential backoff
- Disk cache for fetched pages
- Fuzzy deduplication
- Chunking for large pages
- Stealth mode (playwright-stealth)
- Proxy support

---

## Success Metrics

### Phase 1 (MVP)
- [x] Extract from single URL successfully
- [ ] Extract from 10 URLs in parallel
- [ ] 80%+ success rate on known-good sites
- [ ] <5 sec per page extraction
- [ ] JSON/CSV export working

### Phase 2 (Web UI)
- [ ] Web UI deployed to Vercel
- [ ] User can paste URL → get results
- [ ] Results saved to Supabase
- [ ] Export to CSV working
- [ ] 5+ schemas available

### Phase 3 (Production)
- [ ] 90%+ success rate on diverse sites
- [ ] <10 sec per page extraction (with JS)
- [ ] Handles 100+ URLs in single batch
- [ ] Deduplication working
- [ ] Added to VibeCodersToolbox

---

## Next Steps (Immediate)

1. **Create CLI** (`uberscrape extract <url>`)
2. **Test on real website** (rental listing)
3. **Add batch processing** (multiple URLs)
4. **Implement export formats** (JSON, CSV, Markdown)
5. **Create GitHub repo** and push initial commit
6. **Document usage** with examples

---

## Notes

- Built as standalone package (can publish to PyPI later)
- Designed to be integrated into VibeCodersToolbox
- Follows patterns from Pink Auto Glass invoice parser
- Security-first approach (no keys in code)
- Graceful error handling (one failure ≠ batch failure)

---

## Repository
**GitHub:** https://github.com/dougsimpson/uberscrape (to be created)

---

**Last Updated:** 2026-02-25 10:20 MST by Claude Code
