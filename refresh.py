#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh.py — Build data.json for the Market Monitor dashboard from an
end-of-day market-data API (default: Twelve Data free tier).

Why this version (vs refresh_moomoo.py): no local gateway / personal login,
so it runs in the cloud (GitHub Actions) and the dashboard can be shared
publicly. The API key lives in an env var (a CI secret), never in the browser.

Setup:
  1. Get a free key at https://twelvedata.com  (free tier: 800 calls/day, 8/min)
  2. export TWELVEDATA_API_KEY=your_key
  3. python3 refresh.py            # writes data.json
     python3 refresh.py --serve    # writes data.json, then serves on :8000

No pip install needed (uses only the standard library).

NOTE ON LICENSING: free tiers are for personal/eval use and generally do NOT
permit commercial redistribution. Before you charge for access, upgrade to a
plan whose terms allow redistribution (set PROVIDER/key accordingly).
"""
import os, sys, json, time, datetime as dt
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
OUT  = HERE / "data.json"

API_KEY  = os.environ.get("TWELVEDATA_API_KEY", "").strip()
BASE     = "https://api.twelvedata.com/time_series"
THROTTLE = 7.6          # seconds between calls -> stays under 8 req/min free limit
OUTSIZE  = 400          # daily bars (~ 18 months) to cover the 1Y / YTD lookbacks

# key        = the `sym` value used in index.html (must match exactly)
# td         = provider ticker
# pct        = True  -> render period change as percent
#              False -> render as absolute point/dollar difference
# keep_close = True  -> row shows an index/spot LEVEL the ETF only proxies;
#              overlay the % moves but keep the recognizable static close.
ENTRIES = [
    {"key": "US.SPY",  "td": "SPY",  "pct": True,  "keep_close": True},   # 标普500
    {"key": "US.QQQ",  "td": "QQQ",  "pct": True,  "keep_close": True},   # 纳指
    {"key": "US.DIA",  "td": "DIA",  "pct": True,  "keep_close": True},   # 道指
    {"key": "US.TLT",  "td": "TLT",  "pct": True},                        # 长债
    {"key": "US.GLD",  "td": "GLD",  "pct": True,  "keep_close": True},   # 黄金
    {"key": "US.USO",  "td": "USO",  "pct": True,  "keep_close": True},   # 原油
    {"key": "US.IGV",  "td": "IGV",  "pct": False},                       # 软件(点差)
    {"key": "US.IWM",  "td": "IWM",  "pct": True,  "keep_close": True},   # 罗素2000
    {"key": "US.IXP",  "td": "IXP",  "pct": True},
    {"key": "US.XLY",  "td": "XLY",  "pct": True},
    {"key": "US.XLP",  "td": "XLP",  "pct": True},
    {"key": "US.XLE",  "td": "XLE",  "pct": True},
    {"key": "US.KBWB", "td": "KBWB", "pct": True},
    {"key": "US.XLU",  "td": "XLU",  "pct": True},
    {"key": "US.IYR",  "td": "IYR",  "pct": True},
    {"key": "US.XLK",  "td": "XLK",  "pct": True},
    {"key": "US.XLV",  "td": "XLV",  "pct": True},
    {"key": "US.ITA",  "td": "ITA",  "pct": True},
    {"key": "US.IAK",  "td": "IAK",  "pct": True},
    {"key": "US.SOXX", "td": "SOXX", "pct": True},
    {"key": "US.IWD",  "td": "IWD",  "pct": True},
    {"key": "US.IWF",  "td": "IWF",  "pct": True},
    {"key": "US.MAGS", "td": "MAGS", "pct": True},   # 七巨头 ETF
    {"key": "US.RSP",  "td": "RSP",  "pct": True},
]


def fetch_series(ticker):
    """Return list of (date, close) ascending, or None on failure."""
    q = urlencode({"symbol": ticker, "interval": "1day",
                   "outputsize": OUTSIZE, "apikey": API_KEY})
    with urlopen(f"{BASE}?{q}", timeout=30) as r:
        data = json.load(r)
    if data.get("status") == "error" or "values" not in data:
        raise RuntimeError(data.get("message", "no values"))
    rows = []
    for v in data["values"]:
        try:
            rows.append((dt.date.fromisoformat(v["datetime"][:10]), float(v["close"])))
        except (KeyError, ValueError):
            continue
    rows.sort(key=lambda x: x[0])
    return rows


def ref_close_on_or_before(series, target):
    chosen = None
    for d, c in series:
        if d <= target:
            chosen = c
        else:
            break
    return chosen


def build_quote(series, pct):
    last_d, last = series[-1]
    q = {}
    if len(series) >= 2:
        prev = series[-2][1]
        if prev:
            q["d1"] = round((last / prev - 1) * 100, 1) if pct else round(last - prev, 2)
    today = dt.date.today()
    targets = {
        "w1":  today - dt.timedelta(days=7),
        "m1":  today - dt.timedelta(days=30),
        "y1":  today - dt.timedelta(days=365),
        "qtd": dt.date(today.year, 3 * ((today.month - 1) // 3) + 1, 1) - dt.timedelta(days=1),
        "ytd": dt.date(today.year - 1, 12, 31),
    }
    for k, tgt in targets.items():
        ref = ref_close_on_or_before(series, tgt)
        if ref:
            q[k] = round((last / ref - 1) * 100, 1) if pct else round(last - ref, 2)
    q["close"] = round(last, 2)
    return q


def run_once():
    if not API_KEY:
        print("ERROR: set TWELVEDATA_API_KEY (get a free key at https://twelvedata.com)")
        sys.exit(1)
    quotes, ok, fail = [], [], []
    for i, e in enumerate(ENTRIES):
        try:
            series = fetch_series(e["td"])
            if not series:
                raise RuntimeError("empty series")
            q = build_quote(series, e["pct"])
            q["sym"] = e["key"]
            if e.get("keep_close"):
                q.pop("close", None)
            quotes.append(q)
            ok.append(e["key"])
        except Exception as ex:
            fail.append(f"{e['key']}({ex})")
        if i < len(ENTRIES) - 1:
            time.sleep(THROTTLE)   # respect free-tier rate limit
    payload = {"as_of": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
               "source": "Twelve Data (EOD)", "quotes": quotes}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ wrote {OUT.name}: {len(ok)} ok, {len(fail)} failed")
    if fail:
        print("  failed: " + ", ".join(fail))


def serve():
    import http.server, socketserver, functools
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
    with socketserver.TCPServer(("", 8000), h) as httpd:
        print("Serving at http://localhost:8000/index.html (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    run_once()
    if "--serve" in sys.argv[1:]:
        serve()
