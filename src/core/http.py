from __future__ import annotations  # 타입 힌트 평가를 지연합니다.
from dataclasses import dataclass  # 간결한 데이터 클래스를 만들기 위해 사용합니다.
from typing import Any, Dict, Optional  # 타입 힌트용 타입들을 가져옵니다.
import requests  # HTTP 요청을 수행합니다.

from .logger import get_logger  # 공통 로거 생성 함수를 가져옵니다.
from .retry import retryable  # 재시도 데코레이터를 가져옵니다.

log = get_logger(__name__)  # 모듈 전용 로거를 초기화합니다.


class HttpError(RuntimeError):  # HTTP 에러를 표현하는 커스텀 예외입니다.
    def __init__(self, message: str, status_code: int | None = None, payload: Any | None = None):  # 메시지/상태코드/응답 본문을 저장합니다.
        super().__init__(message)  # 기본 RuntimeError 초기화를 수행합니다.
        self.status_code = status_code  # 상태 코드를 보관합니다.
        self.payload = payload  # 에러 응답 payload를 보관합니다.


@dataclass
class HttpClient:  # API 호출을 단순화하는 HTTP 클라이언트입니다.
    base_url: str  # 요청 대상의 기본 URL입니다.
    token: Optional[str] = None  # Bearer 토큰(선택)입니다.
    timeout_s: float = 3.0  # 기본 타임아웃(초)입니다.

    def _headers(self) -> Dict[str, str]:  # 기본 요청 헤더를 구성합니다.
        h = {"accept": "application/json"}  # JSON 응답을 기대하는 Accept 헤더를 설정합니다.
        if self.token:  # 토큰이 있으면 인증 헤더를 추가합니다.
            h["authorization"] = f"Bearer {self.token}"
        return h  # 완성된 헤더를 반환합니다.

    @retryable(attempts=3, exception_types=(requests.RequestException,))  # 네트워크 계열 예외는 최대 3회 재시도합니다.
    def request(self, method: str, path: str, json: Any | None = None, timeout_s: float | None = None) -> Any:  # 공통 요청 메서드입니다.
        url = self.base_url.rstrip("/") + path  # base_url 마지막 /를 제거해 path와 안전하게 결합합니다.
        t = timeout_s if timeout_s is not None else self.timeout_s  # 호출별 타임아웃이 없으면 기본값을 사용합니다.
        log.info(f"HTTP {method} {url}")  # 요청 메서드/URL을 로그로 남깁니다.
        r = requests.request(method, url, headers=self._headers(), json=json, timeout=t)  # 실제 HTTP 요청을 보냅니다.
        if r.status_code >= 400:  # 4xx/5xx는 실패로 처리합니다.
            try:  # JSON 오류 응답이면 파싱을 시도합니다.
                payload = r.json()
            except Exception:  # JSON이 아니면 원문 텍스트를 저장합니다.
                payload = r.text
            raise HttpError(f"HTTP {r.status_code} {method} {path}", status_code=r.status_code, payload=payload)  # 상세 정보와 함께 예외를 던집니다.
        if r.headers.get("content-type", "").startswith("application/json"):  # JSON 응답이면 딕셔너리/리스트로 반환합니다.
            return r.json()
        return r.text  # 그 외 콘텐츠는 텍스트로 반환합니다.
