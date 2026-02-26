# UberScrape

**AI-powered web scraping that returns structured data, not HTML walls.**

Turn any website into clean, structured JSON/CSV using Gemini AI for intelligent extraction.

![UberScrape Demo](https://img.shields.io/badge/Status-Production%20Ready-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 What It Does

- **Search** → Find websites with specific content
- **Extract** → Get structured JSON/CSV from any URL (not raw HTML)
- **Map** → Discover all URLs on a website
- **Batch** → Process hundreds of pages in parallel

## ✨ Why UberScrape?

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

## 🎯 Features

✅ **LLM-Powered Extraction** — Gemini AI parses pages intelligently  
✅ **Parallel Processing** — Scrape 10+ pages simultaneously  
✅ **JavaScript Rendering** — Handles dynamic sites (Playwright)  
✅ **Structured Output** — JSON, CSV, or Markdown tables  
✅ **Web UI** — Beautiful dark-themed interface  
✅ **CLI** — Command-line tool for automation  
✅ **Schema Templates** — Pre-built schemas for common use cases  
✅ **Error Handling** — Graceful degradation (1 failure ≠ batch failure)  
✅ **Free** — Uses Gemini API (no cost)  

## 📦 Installation

### CLI Usage

```bash
# Clone repo
git clone https://github.com/dougsimpsoncodes/uberscrape.git
cd uberscrape

# Install dependencies
pip3 install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Web UI

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local and add GEMINI_API_KEY

# Run development server
npm run dev
# Open http://localhost:3000
```

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and add to `.env`:
   ```
   GEMINI_API_KEY="your-key-here"
   ```

Free tier includes generous limits (no credit card required).

## 💻 CLI Usage

### Extract from Single URL

```bash
python3 -m uberscrape.cli extract \
  --url "https://example.com/listing" \
  --schema uberscrape/schemas/rental-listing.json \
  --output results.json
```

### Extract from Multiple URLs

```bash
# Create urls.txt with one URL per line
python3 -m uberscrape.cli extract \
  --urls urls.txt \
  --schema uberscrape/schemas/product.json \
  --parallel 10 \
  --output results.csv
```

### Discover URLs from Sitemap

```bash
python3 -m uberscrape.cli map \
  https://docs.example.com \
  --limit 100 \
  --output urls.txt
```

### Advanced Options

```bash
python3 -m uberscrape.cli extract \
  --url "https://spa-site.com" \
  --schema schema.json \
  --output out.json \
  --browser \              # Use Playwright for JS rendering
  --parallel 5 \           # Process 5 URLs at once
  --timeout 60             # 60 second timeout per request
```

## 🌐 Web UI Usage

1. **Start the server:**
   ```bash
   cd web && npm run dev
   ```

2. **Open http://localhost:3000**

3. **Upload Step:**
   - Paste URLs (one per line)
   - Choose or customize schema
   - Configure advanced options (optional)

4. **Results:**
   - Preview extracted data
   - Download as CSV or JSON
   - Start new scrape

## 📋 Schema Definition

Schemas define what data to extract. Format:

```json
{
  "field_name": "type"
}
```

**Supported types:** `string`, `number`, `boolean`, `array`, `object`

### Example Schemas

**Rental Listing:**
```json
{
  "title": "string",
  "price": "number",
  "bedrooms": "number",
  "bathrooms": "number",
  "sqft": "number",
  "address": "string",
  "description": "string"
}
```

**Product:**
```json
{
  "name": "string",
  "price": "number",
  "brand": "string",
  "description": "string",
  "rating": "number",
  "in_stock": "boolean"
}
```

**Article:**
```json
{
  "title": "string",
  "author": "string",
  "date": "string",
  "content": "string",
  "tags": "array"
}
```

Pre-built schemas available in `uberscrape/schemas/`

## 🎨 Web UI Features

- **3-step workflow:** Upload → Processing → Results
- **Schema templates:** Quick-select common patterns
- **Advanced options:**
  - Browser mode (for JavaScript sites)
  - Parallel requests (1-10 concurrent)
- **Export formats:** JSON, CSV
- **Dark theme:** Easy on the eyes
- **Responsive:** Works on desktop & mobile

## 🏗️ Architecture

```
URL → Fetch (httpx or Playwright) 
    → HTML → Markdown (html2text)
    → Gemini 2.5 Flash + schema
    → Structured JSON
    → Export (JSON/CSV)
```

**Why Markdown?**
- 67% fewer tokens than raw HTML
- Removes noise (ads, navigation, scripts)
- Keeps actual content
- Cheaper API calls

## 🔧 Tech Stack

**Python CLI:**
- Python 3.9+
- httpx (async HTTP)
- Playwright (JavaScript rendering)
- Gemini API (Google AI)
- html2text (HTML → Markdown)
- Click (CLI framework)
- Rich (terminal UI)

**Web UI:**
- Next.js 15
- TypeScript
- Tailwind CSS
- Lucide Icons

## 📊 Use Cases

- **Real Estate:** Extract rental listings, property details
- **E-commerce:** Product data, prices, reviews
- **Research:** Academic papers, news articles
- **Lead Generation:** Business directories, contact info
- **Monitoring:** Price tracking, content changes
- **Documentation:** Crawl entire docs sites

## 🚦 Rate Limiting

Gemini API free tier limits:
- 15 requests per minute
- 1,500 requests per day

For higher volume:
- Use paid Gemini tier
- Or switch to Anthropic Claude (requires API key)

## 🐛 Troubleshooting

**"GEMINI_API_KEY not found"**
- Create `.env` file with your API key
- Or set environment variable: `export GEMINI_API_KEY="..."`

**"404 model not found"**
- Check API key is valid
- Verify Gemini 2.5 Flash is available in your region

**Extraction fails on JavaScript sites**
- Add `--browser` flag to use Playwright
- Slower but handles dynamic content

**Rate limit errors**
- Reduce `--parallel` value
- Add delays between batches
- Upgrade to paid tier

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first.

## 👨‍💻 Author

**Doug Simpson** - [dougiefreshcodes@gmail.com](mailto:dougiefreshcodes@gmail.com)

## 🔗 Links

- **GitHub:** https://github.com/dougsimpsoncodes/uberscrape
- **VibeCodersToolbox:** https://vibecoderstoolbox.com

---

**Built for [VibeCodersToolbox](https://vibecoderstoolbox.com)** 🚀
