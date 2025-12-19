from __future__ import annotations
import argparse, json, socket, time
from urllib.parse import urlparse

import requests

def dns_lookup(host: str) -> dict:
    try:
        ip = socket.gethostbyname(host)
        return {"ok": True, "host": host, "ip": ip}
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}

def tcp_connect(host: str, port: int, timeout_s: float) -> dict:
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ms = int((time.time() - t0) * 1000)
            return {"ok": True, "host": host, "port": port, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "host": host, "port": port, "latency_ms": ms, "error": str(e)}

def http_get(url: str, timeout_s: float) -> dict:
    t0 = time.time()
    try:
        r = requests.get(url, timeout=timeout_s)
        ms = int((time.time() - t0) * 1000)
        return {"ok": r.status_code < 400, "url": url, "status_code": r.status_code, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "url": url, "latency_ms": ms, "error": str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--timeout", type=float, default=2.0)
    ap.add_argument("--out", default="reports/day01_net_basics.json")
    args = ap.parse_args()

    items = []
    items.append({"type": "dns", **dns_lookup(args.host)})
    items.append({"type": "tcp", **tcp_connect(args.host, args.port, args.timeout)})
    items.append({"type": "http", **http_get(args.url, args.timeout)})

    ok = all(i.get("ok") for i in items)
    report = {
        "name": "day01_net_basics",
        "generated_at": time.time(),
        "ok": ok,
        "items": items,
    }

    import os
    os.makedirs("reports", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out} ok={ok}")

if __name__ == "__main__":
    main()
