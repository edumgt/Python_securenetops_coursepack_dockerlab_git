from __future__ import annotations  # 타입 힌트 평가를 지연합니다.
from dataclasses import dataclass, asdict  # 보고서 모델 선언과 직렬화에 사용합니다.
from typing import Any, Dict, List  # 타입 힌트에 사용합니다.
from pathlib import Path  # 파일 저장 경로 처리를 담당합니다.
import json  # JSON 직렬화를 위해 사용합니다.
from datetime import datetime, timezone  # UTC 기준 타임스탬프 생성을 위해 사용합니다.


def utcnow_iso() -> str:  # 현재 UTC 시각을 ISO-8601 문자열로 반환합니다.
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Report:  # 공통 리포트 구조체입니다.
    name: str  # 리포트 이름입니다.
    generated_at: str  # 생성 시각(ISO 문자열)입니다.
    ok: bool  # 전체 성공 여부입니다.
    summary: Dict[str, Any]  # 요약 메타데이터입니다.
    items: List[Dict[str, Any]]  # 상세 체크 항목 목록입니다.

    def to_dict(self) -> Dict[str, Any]:  # dataclass를 dict로 변환합니다.
        return asdict(self)


def write_json(path: str | Path, data: Any) -> None:  # 데이터를 예쁘게 들여쓴 JSON 파일로 저장합니다.
    p = Path(path)  # 경로를 Path 객체로 변환합니다.
    p.parent.mkdir(parents=True, exist_ok=True)  # 상위 폴더가 없으면 생성합니다.
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")  # UTF-8 JSON으로 저장합니다.
