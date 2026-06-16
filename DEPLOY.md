# Deploying Market Monitor (share with friends, incl. 🇭🇰 Hong Kong)

This dashboard is a **static site** (`index.html`) plus a **data file** (`data.json`)
that a daily GitHub Action regenerates from a market-data API. No server to run.

```
Twelve Data (free, EOD)  →  GitHub Action (daily cron, key = secret)
                                   │ commits data.json
                                   ▼
                         Cloudflare Pages (global CDN, HK PoP)  →  your friends
```

---

## 1. Get a free data API key (5 min)
1. Sign up at <https://twelvedata.com> → **API Keys** → copy your key.
2. Free tier = 800 calls/day, 8/min. This dashboard uses ~24 calls/refresh — plenty.

> ⚠️ **Before you charge anyone:** free tiers do **not** allow commercial
> redistribution. To monetize, upgrade to a Twelve Data plan (or Polygon.io /
> EODHD) whose terms permit redistribution, then just replace the secret — no
> code change needed.

## 2. Test locally
```bash
cd "Market Monitor"
export TWELVEDATA_API_KEY=your_key_here
python3 refresh.py --serve        # writes data.json, serves on :8000
# open http://localhost:8000/index.html
```

## 3. Put it on GitHub
```bash
cd "Market Monitor"
git init && git add . && git commit -m "Market Monitor dashboard"
# create an empty repo on github.com, then:
git remote add origin https://github.com/<you>/market-monitor.git
git branch -M main && git push -u origin main
```
Then add the API key as a secret:
**GitHub repo → Settings → Secrets and variables → Actions → New repository secret**
- Name: `TWELVEDATA_API_KEY`   Value: *your key*

The Action runs daily at 22:10 UTC (after US close). Run it once now from the
**Actions** tab → *Refresh market data* → *Run workflow* to populate `data.json`.

## 4. Host on Cloudflare Pages (free, works well in HK)
1. <https://dash.cloudflare.com> → **Workers & Pages → Create → Pages →
   Connect to Git** → pick your repo.
2. Build settings: **Framework preset = None**, **Build command = (blank)**,
   **Output directory = `/`** (the site is plain static files).
3. Deploy. You get a public URL like `https://market-monitor.pages.dev`.
4. Every `git push` (including the bot's daily `data.json` commit) auto-redeploys.

**Why Cloudflare Pages for HK:** global Anycast CDN with a Hong Kong edge, no
regional blocking, free tier is generous. (Vercel/Netlify also work; Cloudflare
tends to be the most reliable from mainland-adjacent networks.)

### Optional: custom domain
Cloudflare Pages → your project → **Custom domains** → add `monitor.yourdomain.com`.

---

## Notes
- **Yields / Put-Call / HY spread / VIX / Bitcoin** aren't on the EOD ETF feed,
  so they stay as the labeled static snapshot. Ask if you want VIX/BTC wired in
  (different endpoints) — easy to add.
- **Index/spot rows** (S&P, Nasdaq, Dow, Gold, Oil, Russell 2000) track their
  ETFs: the **% moves are live**, the **close stays the recognizable index level**.
- `refresh_moomoo.py` is your original local moomoo version, kept as a backup.
