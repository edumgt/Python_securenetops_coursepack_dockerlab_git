from __future__ import annotations  # 타입 힌트를 지연 평가합니다.
import os  # 환경변수 조회에 사용합니다.
from typing import Any, Dict, Optional  # 타입 힌트에 사용합니다.
from fastapi import FastAPI, Header, HTTPException  # FastAPI 앱/헤더/예외를 사용합니다.
from pydantic import BaseModel, Field  # 요청 바디 검증 모델을 정의합니다.

app = FastAPI(title="Controller API (Mock)", version="0.2")  # 컨트롤러 모의 API 앱 객체입니다.
TOKEN = os.getenv("CONTROLLER_API_TOKEN", "dev-token-please-change")  # 인증 토큰입니다.

STATE: Dict[str, Any] = {  # 메모리 기반 현재 상태 저장소입니다.
    "firewall_policy": {"target_web_allowed_inbound_ports": [8080]},
    "monitoring_policy": {"web_latency_ms_warn": 250, "web_latency_ms_crit": 600},
}


def require_auth(authorization: Optional[str]) -> None:  # Authorization 헤더를 검증합니다.
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid scheme")
    token = authorization.split(" ", 1)[1].strip()
    if token != TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/health")
def health():  # 헬스 체크 엔드포인트입니다.
    return {"ok": True, "service": "controller_api"}


@app.get("/state")
def get_state(authorization: Optional[str] = Header(default=None)):  # 현재 상태를 조회합니다.
    require_auth(authorization)
    return STATE


class DesiredState(BaseModel):  # 목표 상태 요청 바디 스키마입니다.
    firewall_policy: Dict[str, Any] = Field(default_factory=dict)
    monitoring_policy: Dict[str, Any] = Field(default_factory=dict)


@app.post("/state")
def set_state(body: DesiredState, authorization: Optional[str] = Header(default=None)):  # 목표 상태를 적용합니다.
    require_auth(authorization)
    if body.firewall_policy:
        STATE["firewall_policy"] = body.firewall_policy
    if body.monitoring_policy:
        STATE["monitoring_policy"] = body.monitoring_policy
    return {"ok": True, "state": STATE}
