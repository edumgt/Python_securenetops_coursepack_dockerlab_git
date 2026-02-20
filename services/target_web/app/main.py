from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import time  # 의도적 지연을 만들기 위해 사용합니다.
from fastapi import FastAPI, Response  # FastAPI 앱과 응답 헤더 설정을 사용합니다.

app = FastAPI(title="Target Web (Lab)", version="0.2")  # 실습용 웹 서비스입니다.


@app.get("/health")
def health():  # 헬스 체크 엔드포인트입니다.
    return {"ok": True, "service": "target_web"}


@app.get("/slow")
def slow(ms: int = 200):  # 지연 시나리오 테스트용 엔드포인트입니다.
    time.sleep(ms / 1000.0)
    return {"ok": True, "slept_ms": ms}


@app.get("/")
def root(resp: Response):  # 루트 엔드포인트이며 보안 헤더를 설정합니다.
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    return {"message": "Hello from target_web"}
