from __future__ import annotations  # 타입 힌트 평가를 지연합니다.
from pathlib import Path  # 파일 경로 처리 유틸입니다.
from typing import Any, Dict, Optional  # 타입 힌트를 위해 사용합니다.
import os, yaml  # 환경변수 조회와 YAML 파싱에 사용합니다.


class ConfigError(RuntimeError): ...  # 설정 관련 오류를 나타내는 예외입니다.


def load_yaml(path: str | Path) -> Dict[str, Any]:  # YAML 파일을 읽어 딕셔너리로 반환합니다.
    p = Path(path)  # 입력 경로를 Path 객체로 정규화합니다.
    if not p.exists():  # 파일이 없으면 즉시 명확한 예외를 발생시킵니다.
        raise ConfigError(f"Config file not found: {p}")
    data = yaml.safe_load(p.read_text(encoding="utf-8"))  # UTF-8 텍스트를 읽어 안전하게 YAML 파싱합니다.
    return data or {}  # 빈 파일(None)일 경우 빈 dict를 반환합니다.


def env(name: str, default: Optional[str] = None) -> str:  # 환경변수를 읽고 없으면 예외를 발생시킵니다.
    v = os.getenv(name, default)  # 환경변수를 조회합니다.
    if v is None:  # 기본값도 없고 환경변수도 없으면 실패 처리합니다.
        raise ConfigError(f"Missing env var: {name}")
    return v  # 문자열 값을 반환합니다.
