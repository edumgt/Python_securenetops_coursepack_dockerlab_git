from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import argparse, socket, time, re  # CLI/소켓/시간/정규식 모듈을 사용합니다.
from typing import Any, Dict, List  # 타입 힌트에 사용합니다.
import requests  # HTTP 헤더 점검을 위해 사용합니다.

from src.core.config import load_yaml, env  # 정책 파일 로드와 환경변수 조회를 사용합니다.
from src.core.logger import get_logger  # 공통 로거입니다.
from src.core.report import Report, utcnow_iso, write_json  # 리포트 생성 유틸입니다.

log = get_logger(__name__)  # 모듈 로거를 초기화합니다.


def tcp_connect(host: str, port: int, timeout_s: float = 1.0) -> Dict[str, Any]:  # TCP 연결 가능성과 지연을 측정합니다.
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            ms = int((time.time() - t0) * 1000)
            return {"ok": True, "host": host, "port": port, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "host": host, "port": port, "latency_ms": ms, "error": str(e)}


def get_headers(url: str, timeout_s: float = 2.0) -> Dict[str, Any]:  # URL 응답 헤더를 수집합니다.
    try:
        r = requests.get(url, timeout=timeout_s)
        return {"ok": r.status_code < 500, "url": url, "status_code": r.status_code, "headers": {k.lower(): v for k, v in r.headers.items()}}
    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)}


def main():  # 보안 점검 엔트리 포인트입니다.
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="configs/security_policy.yml")  # 보안 정책 파일 경로입니다.
    ap.add_argument("--report", default="reports/security_report.json")  # 출력 리포트 경로입니다.
    args = ap.parse_args()

    pol = load_yaml(args.policy).get("policy", {})  # policy 섹션만 추출합니다.
    items: List[Dict[str, Any]] = []  # 결과 항목을 누적합니다.

    for ep in (pol.get("allowlisted_endpoints", []) or []):  # 허용된 엔드포인트 목록을 순회합니다.
        for p in (ep.get("ports", []) or []):
            items.append({"check": "allowlisted_port", "name": ep["name"], **tcp_connect(ep["host"], int(p), 1.0)})

    required = [h.lower() for h in (pol.get("http_headers_required", []) or [])]  # 필수 헤더 목록을 소문자로 정규화합니다.
    for url in ["http://172.30.0.20:8080/", "http://172.30.0.20:8080/health"]:  # 타겟 웹 주요 엔드포인트를 검사합니다.
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

    forbid = pol.get("secrets_rules", {}).get("forbid_patterns", []) or []  # 로그에 나오면 안 되는 문자열 패턴입니다.
    sample = [f"controller token={env('CONTROLLER_API_TOKEN', '')}", "sample log line"]  # 간단한 샘플 로그를 구성합니다.
    leaks = []
    for pat in forbid:  # 금지 패턴이 샘플 텍스트에 나타나는지 검사합니다.
        rx = re.compile(re.escape(pat))
        for t in sample:
            if rx.search(t):
                leaks.append({"pattern": pat, "text": t})
    items.append({"check": "secret_leak_guard", "ok": len(leaks) == 0, "leaks": leaks})

    ok = True  # 전체 성공 여부를 수동 규칙으로 집계합니다.
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
