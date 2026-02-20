from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import argparse, json, os, time  # CLI/JSON/파일시스템/시간 모듈을 사용합니다.
from dataclasses import dataclass  # 타겟 정의를 위해 dataclass를 사용합니다.
from typing import Any, Dict, List  # 타입 힌트에 사용합니다.
import requests  # 웹 상태를 측정하고 웹훅을 호출합니다.

from src.core.config import load_yaml  # 모니터 설정 로더입니다.
from src.core.logger import get_logger  # 공통 로거를 사용합니다.

log = get_logger(__name__)  # 모듈 로거를 초기화합니다.


@dataclass
class Target:  # 모니터링 대상 한 건을 표현합니다.
    name: str  # 대상 이름입니다.
    url: str  # 측정 URL입니다.
    timeout_s: float  # 요청 타임아웃입니다.
    warn_ms: int  # 경고 지연 기준(ms)입니다.
    crit_ms: int  # 치명 지연 기준(ms)입니다.


def post_webhook(url: str, payload: Dict[str, Any]) -> None:  # 경고/치명 이벤트를 웹훅으로 전송합니다.
    try:
        requests.post(url, json=payload, timeout=2.5)  # 웹훅 전송 실패가 루프를 깨지 않도록 짧은 timeout을 둡니다.
    except Exception as e:
        log.warning(f"webhook failed: {e}")


def measure(url: str, timeout_s: float) -> Dict[str, Any]:  # 단일 URL 응답 상태와 지연을 측정합니다.
    t0 = time.time()  # 시작 시각입니다.
    try:
        r = requests.get(url, timeout=timeout_s)  # 대상 URL을 호출합니다.
        ms = int((time.time() - t0) * 1000)
        return {"ok": r.status_code < 500, "status_code": r.status_code, "latency_ms": ms}
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {"ok": False, "latency_ms": ms, "error": str(e)}


def main():  # 모니터 에이전트 엔트리 포인트입니다.
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/monitor.yml")  # 모니터 설정 경로입니다.
    args = ap.parse_args()

    cfg = load_yaml(args.config).get("monitor", {})  # monitor 섹션만 추출합니다.
    interval = int(cfg.get("interval_s", 5))  # 측정 주기(초)입니다.
    metrics_path = cfg.get("metrics_path", "/data/metrics.jsonl")  # JSONL 메트릭 파일 경로입니다.
    alert_enabled = bool(cfg.get("alert", {}).get("enabled", True))  # 알림 활성화 여부입니다.
    webhook = os.getenv("ALERT_WEBHOOK_URL", "").strip()  # 선택적 웹훅 URL입니다.

    targets: List[Target] = []  # 타겟 목록을 구성합니다.
    for t in (cfg.get("targets", []) or []):
        targets.append(Target(t["name"], t["url"], float(t.get("timeout_s", 2)), int(t.get("warn_ms", 250)), int(t.get("crit_ms", 600))))

    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)  # 메트릭 디렉터리를 미리 생성합니다.
    log.info(f"monitor_agent started interval={interval}s targets={len(targets)}")

    while True:  # 에이전트는 계속 측정합니다.
        now = int(time.time())  # 이벤트 타임스탬프(초)입니다.
        for t in targets:  # 각 대상에 대해 측정합니다.
            res = measure(t.url, t.timeout_s)
            sev = "ok"  # 기본 심각도는 ok입니다.
            if not res.get("ok"):
                sev = "crit"  # 요청 실패면 치명으로 분류합니다.
            else:
                ms = int(res.get("latency_ms", 0))
                if ms >= t.crit_ms:
                    sev = "crit"
                elif ms >= t.warn_ms:
                    sev = "warn"
            event = {"ts": now, "name": t.name, "url": t.url, "severity": sev, **res}  # 이벤트 레코드를 구성합니다.
            with open(metrics_path, "a", encoding="utf-8") as f:  # JSONL에 append 저장합니다.
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            if alert_enabled and sev in ("warn", "crit"):  # 경고/치명 이벤트만 알림을 전송합니다.
                msg = {"text": f"[{sev.upper()}] {t.name} latency={event.get('latency_ms')}ms ok={event.get('ok')}", "event": event}
                log.warning(msg["text"])
                if webhook:
                    post_webhook(webhook, msg)
        time.sleep(interval)  # 다음 주기까지 대기합니다.


if __name__ == "__main__":
    main()
