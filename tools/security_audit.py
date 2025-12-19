from __future__ import annotations
import argparse, socket, time, re
from typing import Any, Dict, List
import requests

from src.core.config import load_yaml, env
from src.core.logger import get_logger
from src.core.report import Report, utcnow_iso, write_json

log = get_logger(__name__)

def tcp_connect(host: str, port: int, timeout_s: float = 1.0) -> Dict[str, Any]:
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ms = int((time.time()-t0)*1000)
            return {"ok": True, "host": host, "port": port, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time()-t0)*1000)
        return {"ok": False, "host": host, "port": port, "latency_ms": ms, "error": str(e)}

def get_headers(url: str, timeout_s: float = 2.0) -> Dict[str, Any]:
    try:
        r = requests.get(url, timeout=timeout_s)
        return {"ok": r.status_code < 500, "url": url, "status_code": r.status_code,
                "headers": {k.lower(): v for k, v in r.headers.items()}}
    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="configs/security_policy.yml")
    ap.add_argument("--report", default="reports/security_report.json")
    args = ap.parse_args()

    pol = load_yaml(args.policy).get("policy", {})
    items: List[Dict[str, Any]] = []

    # 1) allowlisted ports only
    for ep in (pol.get("allowlisted_endpoints", []) or []):
        for p in (ep.get("ports", []) or []):
            items.append({"check":"allowlisted_port","name":ep["name"], **tcp_connect(ep["host"], int(p), 1.0)})

    # 2) http headers
    required = [h.lower() for h in (pol.get("http_headers_required", []) or [])]
    for url in ["http://172.30.0.20:8080/", "http://172.30.0.20:8080/health"]:
        r = get_headers(url, 2.0)
        missing = []
        if r.get("ok") and "headers" in r:
            for h in required:
                if h not in r["headers"]:
                    missing.append(h)
        r["check"] = "http_headers"
        r["missing_required_headers"] = missing
        r["severity"] = "warning" if missing else "ok"
        items.append(r)

    # 3) secret leak guard (discipline)
    forbid = pol.get("secrets_rules", {}).get("forbid_patterns", []) or []
    sample = [f"controller token={env('CONTROLLER_API_TOKEN','')}", "sample log line"]
    leaks = []
    for pat in forbid:
        rx = re.compile(re.escape(pat))
        for t in sample:
            if rx.search(t):
                leaks.append({"pattern": pat, "text": t})
    items.append({"check":"secret_leak_guard","ok": len(leaks)==0, "leaks": leaks})

    ok = True
    for it in items:
        if it.get("check") == "allowlisted_port" and not it.get("ok"):
            ok = False
        if it.get("check") == "secret_leak_guard" and not it.get("ok"):
            ok = False

    rep = Report("security_audit", utcnow_iso(), ok, {"required_headers": required}, items)
    write_json(args.report, rep.to_dict())
    log.info(f"Wrote report: {args.report} ok={ok}")

if __name__ == "__main__":
    main()
