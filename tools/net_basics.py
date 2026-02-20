from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import argparse, json, socket, time  # CLI/JSON/소켓/시간 모듈을 사용합니다.

import requests  # HTTP 체크에 사용합니다.


def dns_lookup(host: str) -> dict:  # DNS 질의를 수행합니다.
    try:
        ip = socket.gethostbyname(host)
        return {"ok": True, "host": host, "ip": ip}
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}


def tcp_connect(host: str, port: int, timeout_s: float) -> dict:  # TCP 연결 테스트를 수행합니다.
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ms = int((time.time() - t0) * 1000)
            return {"ok": True, "host": host, "port": port, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "host": host, "port": port, "latency_ms": ms, "error": str(e)}


def http_get(url: str, timeout_s: float) -> dict:  # HTTP GET 테스트를 수행합니다.
    t0 = time.time()
    try:
        r = requests.get(url, timeout=timeout_s)
        ms = int((time.time() - t0) * 1000)
        return {"ok": r.status_code < 400, "url": url, "status_code": r.status_code, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "url": url, "latency_ms": ms, "error": str(e)}


def main():  # Day01 진단 스크립트 엔트리 포인트입니다.
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)  # DNS/TCP 대상 호스트입니다.
    ap.add_argument("--port", type=int, required=True)  # TCP 대상 포트입니다.
    ap.add_argument("--url", required=True)  # HTTP 대상 URL입니다.
    ap.add_argument("--timeout", type=float, default=2.0)  # 공통 타임아웃(초)입니다.
    ap.add_argument("--out", default="reports/day01_net_basics.json")  # 리포트 출력 경로입니다.
    args = ap.parse_args()

    items = []
    items.append({"type": "dns", **dns_lookup(args.host)})  # DNS 결과를 누적합니다.
    items.append({"type": "tcp", **tcp_connect(args.host, args.port, args.timeout)})  # TCP 결과를 누적합니다.
    items.append({"type": "http", **http_get(args.url, args.timeout)})  # HTTP 결과를 누적합니다.

    ok = all(i.get("ok") for i in items)  # 모든 항목 성공 시 true입니다.
    report = {  # 최종 리포트 객체입니다.
        "name": "day01_net_basics",
        "generated_at": time.time(),
        "ok": ok,
        "items": items,
    }

    import os  # 리포트 디렉터리 생성을 위해 로컬 import를 사용합니다.
    os.makedirs("reports", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out} ok={ok}")


if __name__ == "__main__":
    main()
