from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import argparse  # CLI 인자 파싱에 사용합니다.
from typing import Any, Dict, List  # 타입 힌트에 사용합니다.

from src.core.config import load_yaml, env  # 설정 로딩과 환경변수 조회를 사용합니다.
from src.core.http import HttpClient, HttpError  # 컨트롤러 API 호출용 HTTP 클라이언트와 예외입니다.
from src.core.logger import get_logger  # 공통 로거를 사용합니다.
from src.core.report import Report, utcnow_iso, write_json  # 리포트 생성/저장 유틸입니다.

log = get_logger(__name__)  # 모듈 로거를 초기화합니다.


def main():  # Intent 적용 엔트리 포인트입니다.
    ap = argparse.ArgumentParser()
    ap.add_argument("--desired", default="configs/desired_state.yml")  # 목표 상태 파일 경로입니다.
    ap.add_argument("--report", default="reports/intent_report.json")  # 결과 리포트 경로입니다.
    args = ap.parse_args()

    token = env("CONTROLLER_API_TOKEN", "dev-token-please-change")  # 컨트롤러 토큰을 읽습니다.
    desired = load_yaml(args.desired).get("desired_state", {})  # desired_state 섹션을 읽습니다.
    cli = HttpClient("http://172.30.0.10:8000", token=token, timeout_s=3)  # 컨트롤러 API 클라이언트를 생성합니다.

    items: List[Dict[str, Any]] = []  # 작업 단계를 기록할 목록입니다.

    try:
        current = cli.request("GET", "/state", timeout_s=2)  # 현재 상태를 조회합니다.
        items.append({"step": "get_current", "ok": True, "current": current})
    except Exception as e:
        items.append({"step": "get_current", "ok": False, "error": str(e)})  # 현재 상태를 못 읽으면 즉시 실패 리포트를 씁니다.
        rep = Report("intent_apply", utcnow_iso(), False, {"reason": "cannot read current"}, items)
        write_json(args.report, rep.to_dict())
        raise

    diff: Dict[str, Any] = {}  # current와 desired의 차이를 담습니다.
    for k, v in desired.items():
        if current.get(k) != v:
            diff[k] = {"from": current.get(k), "to": v}
    items.append({"step": "diff", "ok": True, "diff": diff})

    if diff:  # 차이가 있을 때만 적용 API를 호출합니다.
        try:
            res = cli.request("POST", "/state", json=desired, timeout_s=3)
            items.append({"step": "apply", "ok": True, "result": res})
        except HttpError as e:
            items.append({"step": "apply", "ok": False, "status_code": e.status_code, "payload": e.payload})
        except Exception as e:
            items.append({"step": "apply", "ok": False, "error": str(e)})
    else:
        items.append({"step": "apply", "ok": True, "result": "already converged"})

    after = cli.request("GET", "/state", timeout_s=2)  # 적용 후 상태를 재조회합니다.
    ok = all(after.get(k) == v for k, v in desired.items())  # 목표 상태와 동일한지 검증합니다.
    items.append({"step": "verify", "ok": ok, "state": after})

    rep = Report("intent_apply", utcnow_iso(), ok, {"changed": bool(diff)}, items)
    write_json(args.report, rep.to_dict())
    log.info(f"Wrote report: {args.report} ok={ok}")


if __name__ == "__main__":
    main()
