# UberScrape Deployment Guide

## Quick Deploy to Vercel

### Prerequisites
- Vercel account (free)
- Gemini API key
- GitHub repository

### Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to web directory**
   ```bash
   cd web
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Follow prompts:**
   - Set up and deploy? **Y**
   - Which scope? **(select your account)**
   - Link to existing project? **N**
   - Project name: **uberscrape**
   - Directory: **./web**
   - Override settings? **N**

5. **Add environment variable:**
   - Go to Vercel dashboard
   - Select project → Settings → Environment Variables
   - Add: `GEMINI_API_KEY` = your API key
   - Add to: Production, Preview, Development

6. **Redeploy**
   ```bash
   vercel --prod
   ```

### Custom Domain (Optional)

1. In Vercel dashboard → Settings → Domains
2. Add your domain
3. Update DNS records as instructed

---

## Deploy to Railway (Alternative)

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   cd web
   railway init
   ```

4. **Add environment variable**
   ```bash
   railway variables set GEMINI_API_KEY=your-key
   ```

5. **Deploy**
   ```bash
   railway up
   ```

---

## Local Development

### Web UI
```bash
cd web
npm install
npm run dev
# Open http://localhost:3000
```

### CLI Only
```bash
# From project root
export GEMINI_API_KEY="your-key"
python3 -m uberscrape.cli extract --url https://example.com --schema schema.json --output out.json
```

---

## Environment Variables

### Required
- `GEMINI_API_KEY` — Your Gemini API key

### Optional
- `NODE_ENV` — production (auto-set by Vercel)
- `PORT` — Server port (default: 3000)

---

## Troubleshooting

### "Module not found" errors
```bash
cd web
rm -rf node_modules package-lock.json
npm install
```

### API key not working
- Verify key in Vercel dashboard
- Check key is valid in Google AI Studio
- Ensure environment variable name is exact: `GEMINI_API_KEY`

### Python command not found
Vercel builds are Node.js-only by default. The Python CLI must be available in the deployment environment. Options:

1. **Use Vercel's Python runtime** (add `runtime: python3.9` to vercel.json)
2. **Deploy CLI separately** (Docker, VM)
3. **Use Next.js API route only** (current setup works if Python is in PATH)

---

## Production Checklist

- [ ] Environment variables set
- [ ] Build succeeds (`npm run build`)
- [ ] API endpoint tested (`/api/scrape`)
- [ ] Custom domain configured (optional)
- [ ] Analytics added (optional)
- [ ] Error monitoring setup (Sentry, optional)

---

## Performance Optimization

### For High Volume

1. **Increase timeout**
   - Edit `web/app/api/scrape/route.ts`
   - Change `timeout: 180000` to higher value

2. **Add caching**
   - Implement Redis for fetched pages
   - Cache Gemini responses

3. **Queue system**
   - Use BullMQ or similar
   - Process jobs asynchronously

### For Speed

1. **Disable browser mode by default**
   - Faster fetching with httpx
   - Only use Playwright when needed

2. **Increase parallel requests**
   - Default is 5, can go up to 10
   - Balance speed vs rate limits

---

## Monitoring

### Vercel Analytics
- Enable in dashboard → Analytics
- Track usage, errors, performance

### Custom Logging
Add to `web/app/api/scrape/route.ts`:
```typescript
console.log(`Scraping ${urls.length} URLs with ${parallel} workers`);
```

View logs: `vercel logs`

---

## Updates & Maintenance

### Deploy new version
```bash
git add .
git commit -m "Update message"
git push origin main
vercel --prod
```

### Rollback
```bash
vercel rollback
```

---

## Cost Estimates

### Free Tier (Vercel Hobby)
- **Bandwidth:** 100 GB/month
- **Builds:** Unlimited
- **Functions:** 100 GB-hours/month
- **Enough for:** ~10,000 scrapes/month

### Paid Tier (Vercel Pro - $20/mo)
- **Bandwidth:** 1 TB/month
- **Builds:** Unlimited
- **Functions:** 1,000 GB-hours/month
- **Enough for:** ~100,000 scrapes/month

### Gemini API
- **Free tier:** 15 req/min, 1,500 req/day
- **Paid tier:** Higher limits, pay per use

---

## Security

### API Key Protection
- Never commit `.env` files
- Use Vercel environment variables
- Rotate keys periodically

### Rate Limiting
Add to `web/app/api/scrape/route.ts`:
```typescript
// Simple rate limit by IP
const rateLimit = new Map();
const ip = request.ip;
const now = Date.now();
const lastRequest = rateLimit.get(ip) || 0;

if (now - lastRequest < 10000) { // 10 sec cooldown
  return NextResponse.json({ error: 'Rate limit exceeded' }, { status: 429 });
}
rateLimit.set(ip, now);
```

---

## Support

**Issues:** https://github.com/dougsimpsoncodes/uberscrape/issues  
**Email:** dougiefreshcodes@gmail.com
