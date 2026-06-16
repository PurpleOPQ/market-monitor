#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh.py — Pull real-time quotes from moomoo/Futu OpenD and write data.json
that the dashboard (index.html) overlays onto its static snapshot.

Prereqs:
  1. Futu/moomoo OpenD running and LOGGED IN  (gateway on 127.0.0.1:11111)
  2. US market quote permission on your account
  3. pip package `moomoo` (already installed: v10.x)

Usage:
  python3 refresh.py            # fetch once, write data.json
  python3 refresh.py --serve    # fetch, write, then serve folder on :8000
  python3 refresh.py --loop 60  # refresh every 60s (also serves on :8000)

Then open  http://localhost:8000/index.html  (NOT file://, so fetch works).
"""
import sys, json, time, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT  = HERE / "data.json"
HOST, PORT = "127.0.0.1", 11111

try:
    from moomoo import OpenQuoteContext, RET_OK, KLType, AuType
except Exception as e:
    print("ERROR: cannot import moomoo SDK:", e)
    print("Install with:  pip3 install moomoo")
    sys.exit(1)

# key   = the `sym` value used in index.html (must match exactly to be applied)
# fetch = candidate moomoo codes, tried in order until one returns data
# pct   = True  -> period change rendered as percent
#         False -> period change rendered as absolute point/dollar difference
# keep_close = True -> ETF tracks an index/spot LEVEL whose price differs from the
#              displayed number; overlay only the % moves, keep the static close.
ENTRIES = [
    # ---- macro & assets ----
    {"key": "US.SPY",  "fetch": ["US.SPY"],  "pct": True,  "keep_close": True},   # 标普500 (SPY proxy)
    {"key": "US.QQQ",  "fetch": ["US.QQQ"],  "pct": True,  "keep_close": True},   # 纳指 (QQQ proxy)
    {"key": "US.DIA",  "fetch": ["US.DIA"],  "pct": True,  "keep_close": True},   # 道指 (DIA proxy)
    {"key": "US.TLT",  "fetch": ["US.TLT"],  "pct": True},                        # 长债
    {"key": "US.GLD",  "fetch": ["US.GLD"],  "pct": True,  "keep_close": True},   # 黄金 (GLD proxy)
    {"key": "US.USO",  "fetch": ["US.USO"],  "pct": True,  "keep_close": True},   # 原油 (USO proxy)
    {"key": "US.IGV",  "fetch": ["US.IGV"],  "pct": False},                       # 软件(点差)
    {"key": "US.IWM",  "fetch": ["US.IWM"],  "pct": True,  "keep_close": True},   # 罗素2000 (IWM proxy)
    # ---- sectors ----
    {"key": "US.IXP",  "fetch": ["US.IXP"],  "pct": True},
    {"key": "US.XLY",  "fetch": ["US.XLY"],  "pct": True},
    {"key": "US.XLP",  "fetch": ["US.XLP"],  "pct": True},
    {"key": "US.XLE",  "fetch": ["US.XLE"],  "pct": True},
    {"key": "US.KBWB", "fetch": ["US.KBWB"], "pct": True},
    {"key": "US.XLU",  "fetch": ["US.XLU"],  "pct": True},
    {"key": "US.IYR",  "fetch": ["US.IYR"],  "pct": True},
    {"key": "US.XLK",  "fetch": ["US.XLK"],  "pct": True},
    {"key": "US.XLV",  "fetch": ["US.XLV"],  "pct": True},
    {"key": "US.ITA",  "fetch": ["US.ITA"],  "pct": True},
    {"key": "US.IAK",  "fetch": ["US.IAK"],  "pct": True},
    {"key": "US.SOXX", "fetch": ["US.SOXX"], "pct": True},
    {"key": "US.IWD",  "fetch": ["US.IWD"],  "pct": True},
    {"key": "US.IWF",  "fetch": ["US.IWF"],  "pct": True},
    {"key": "US.MAGS", "fetch": ["US.MAGS"], "pct": True},   # 七巨头 ETF
    {"key": "US.RSP",  "fetch": ["US.RSP"],  "pct": True},
]


def ref_close_on_or_before(df, target):
    """Last available close at or before target date (df sorted ascending)."""
    sub = df[df["d"] <= target]
    if len(sub) == 0:
        return None
    return float(sub.iloc[-1]["close"])


def period_changes(df, last, pct):
    """df: DataFrame with columns d(date), close — ascending. last: latest price."""
    today = dt.date.today()
    targets = {
        "w1":  today - dt.timedelta(days=7),
        "m1":  today - dt.timedelta(days=30),
        "y1":  today - dt.timedelta(days=365),
        "qtd": dt.date(today.year, 3 * ((today.month - 1) // 3) + 1, 1) - dt.timedelta(days=1),
        "ytd": dt.date(today.year - 1, 12, 31),
    }
    out = {}
    for k, tgt in targets.items():
        ref = ref_close_on_or_before(df, tgt)
        if ref is None or ref == 0:
            continue
        out[k] = round((last / ref - 1) * 100, 1) if pct else round(last - ref, 2)
    return out


def fetch_one(ctx, code, pct):
    # snapshot -> last price + today's change
    ret, snap = ctx.get_market_snapshot([code])
    if ret != RET_OK or snap is None or len(snap) == 0:
        return None
    row = snap.iloc[0]
    last = row.get("last_price")
    prev = row.get("prev_close_price")
    if last is None or last != last:  # NaN check
        return None
    last = float(last)
    q = {"close": round(last, 2)}
    if prev and prev == prev and float(prev) != 0:
        q["d1"] = round((last / float(prev) - 1) * 100, 1) if pct else round(last - float(prev), 2)

    # daily klines -> period changes
    end = dt.date.today().isoformat()
    start = (dt.date.today() - dt.timedelta(days=420)).isoformat()
    ret, kl, _ = ctx.request_history_kline(
        code, start=start, end=end, ktype=KLType.K_DAY, autype=AuType.QFQ,
        max_count=1000)
    if ret == RET_OK and kl is not None and len(kl) > 1:
        kl = kl.copy()
        kl["d"] = kl["time_key"].str.slice(0, 10).map(lambda s: dt.date.fromisoformat(s))
        kl = kl[["d", "close"]].sort_values("d").reset_index(drop=True)
        q.update(period_changes(kl, last, pct))
    return q


def fetch_all():
    ctx = OpenQuoteContext(host=HOST, port=PORT)
    quotes, ok, fail = [], [], []
    try:
        for e in ENTRIES:
            got = None
            used = None
            for code in e["fetch"]:
                try:
                    got = fetch_one(ctx, code, e["pct"])
                except Exception as ex:
                    got = None
                if got:
                    used = code
                    break
            if got:
                got["sym"] = e["key"]
                if e.get("keep_close"):
                    got.pop("close", None)   # keep recognizable static level; only overlay % moves
                quotes.append(got)
                ok.append(f"{e['key']}<-{used}")
            else:
                fail.append(e["key"])
    finally:
        ctx.close()
    return quotes, ok, fail


def write(quotes):
    payload = {
        "as_of": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": quotes,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_once():
    print(f"[{dt.datetime.now():%H:%M:%S}] connecting to OpenD {HOST}:{PORT} ...")
    quotes, ok, fail = fetch_all()
    write(quotes)
    print(f"  ✓ updated {len(ok)} symbols -> {OUT.name}")
    if ok:
        print("    ok:  " + ", ".join(ok))
    if fail:
        print("    ✗ no data (kept static): " + ", ".join(fail))


def serve():
    import http.server, socketserver, functools
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("Serving dashboard at  http://localhost:8000/index.html  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--loop" in args:
        every = int(args[args.index("--loop") + 1]) if len(args) > args.index("--loop") + 1 else 60
        import threading
        threading.Thread(target=serve, daemon=True).start()
        try:
            while True:
                try:
                    run_once()
                except Exception as ex:
                    print("  refresh error:", ex)
                time.sleep(every)
        except KeyboardInterrupt:
            print("\nstopped.")
    elif "--serve" in args:
        run_once()
        serve()
    else:
        run_once()
