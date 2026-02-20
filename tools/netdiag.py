from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import argparse, socket, time  # CLI 파싱, 소켓 진단, 시간 측정을 위해 사용합니다.
from typing import Any, Dict, List  # 타입 힌트에 사용합니다.
import requests  # HTTP 체크를 위해 사용합니다.

from src.core.config import load_yaml  # 대상 설정 YAML 로더입니다.
from src.core.logger import get_logger  # 공통 로거를 가져옵니다.
from src.core.report import Report, utcnow_iso, write_json  # 리포트 모델/저장 유틸입니다.

log = get_logger(__name__)  # 모듈 로거를 초기화합니다.


def check_dns(hostname: str) -> Dict[str, Any]:  # DNS 해석 성공 여부를 점검합니다.
    try:
        ip = socket.gethostbyname(hostname)  # 호스트명을 IPv4 주소로 해석합니다.
        return {"type": "dns", "hostname": hostname, "ok": True, "ip": ip}
    except Exception as e:
        return {"type": "dns", "hostname": hostname, "ok": False, "error": str(e)}


def check_tcp(host: str, port: int, timeout_s: float) -> Dict[str, Any]:  # TCP 포트 접속 가능 여부를 점검합니다.
    t0 = time.time()  # 시작 시각을 기록해 지연시간을 계산합니다.
    try:
        with socket.create_connection((host, port), timeout=timeout_s):  # timeout 내 연결을 시도합니다.
            ms = int((time.time() - t0) * 1000)  # 밀리초 단위 지연시간을 계산합니다.
            return {"type": "tcp", "host": host, "port": port, "ok": True, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"type": "tcp", "host": host, "port": port, "ok": False, "latency_ms": ms, "error": str(e)}


def check_http(url: str, timeout_s: float) -> Dict[str, Any]:  # HTTP 응답 상태/지연을 점검합니다.
    t0 = time.time()  # 시작 시각을 기록합니다.
    try:
        r = requests.get(url, timeout=timeout_s)  # GET 요청을 보냅니다.
        ms = int((time.time() - t0) * 1000)
        return {"type": "http", "url": url, "ok": r.status_code < 400, "status_code": r.status_code, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"type": "http", "url": url, "ok": False, "latency_ms": ms, "error": str(e)}


def main():  # 엔트리 포인트입니다.
    ap = argparse.ArgumentParser()  # CLI 파서를 생성합니다.
    ap.add_argument("--targets", default="configs/targets.yml")  # 점검 대상 설정 파일입니다.
    ap.add_argument("--report", default="reports/netdiag.json")  # 결과 리포트 파일 경로입니다.
    args = ap.parse_args()  # 인자를 파싱합니다.

    cfg = load_yaml(args.targets)  # YAML 설정을 읽습니다.
    items: List[Dict[str, Any]] = []  # 체크 결과를 누적합니다.

    for it in (cfg.get("checks", {}).get("dns", []) or []):  # DNS 체크 목록을 순회합니다.
        items.append(check_dns(it["hostname"]))
    for it in (cfg.get("checks", {}).get("tcp", []) or []):  # TCP 체크 목록을 순회합니다.
        items.append(check_tcp(it["host"], int(it["port"]), float(it.get("timeout_s", 1))))
    for it in (cfg.get("checks", {}).get("http", []) or []):  # HTTP 체크 목록을 순회합니다.
        items.append(check_http(it["url"], float(it.get("timeout_s", 2))))

    ok = all(x.get("ok") for x in items) if items else False  # 항목이 하나라도 실패하면 전체 실패입니다.
    summary = {"total": len(items), "ok": sum(1 for x in items if x.get("ok")), "fail": sum(1 for x in items if not x.get("ok"))}  # 요약 통계를 계산합니다.
    rep = Report("netdiag", utcnow_iso(), ok, summary, items)  # 리포트 객체를 생성합니다.
    write_json(args.report, rep.to_dict())  # JSON 파일로 저장합니다.
    log.info(f"Wrote report: {args.report} ok={ok}")  # 저장 결과를 로그로 남깁니다.


if __name__ == "__main__":  # 스크립트 직접 실행 시 main을 호출합니다.
    main()
