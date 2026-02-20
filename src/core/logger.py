from __future__ import annotations  # 타입 힌트 평가를 지연합니다.
import logging, os, re  # 로깅, 환경변수, 정규식 모듈을 사용합니다.
from typing import Iterable, List  # 타입 힌트에 사용합니다.

DEFAULT_MASK_KEYS = ["token", "authorization", "password", "secret", "api_key"]  # 마스킹할 기본 키 목록입니다.


def _patterns(extra: Iterable[str] | None) -> List[re.Pattern]:  # 메시지 마스킹용 패턴 리스트를 구성합니다.
    ps: List[re.Pattern] = []  # 최종 패턴 목록입니다.
    for k in DEFAULT_MASK_KEYS:  # 기본 키마다 'key=value' 패턴을 추가합니다.
        ps.append(re.compile(rf"({k}\s*[:=]\s*)([^\s,;]+)", re.IGNORECASE))
    if extra:  # 추가 비밀값이 주어지면 값 자체를 마스킹하는 패턴도 만듭니다.
        for s in extra:
            if s:
                ps.append(re.compile(re.escape(s)))
    return ps  # 완성된 패턴 리스트를 반환합니다.


class MaskingFormatter(logging.Formatter):  # 민감정보를 치환하는 커스텀 포매터입니다.
    def __init__(self, fmt: str, extra_secrets: Iterable[str] | None = None):  # 포맷 문자열과 추가 비밀값을 받습니다.
        super().__init__(fmt)  # 부모 Formatter를 초기화합니다.
        self.ps = _patterns(extra_secrets)  # 마스킹 패턴을 준비해 둡니다.

    def format(self, record: logging.LogRecord) -> str:  # 로그 레코드를 문자열로 변환 후 마스킹합니다.
        msg = super().format(record)  # 기본 포맷 결과 문자열을 만듭니다.
        for p in self.ps:  # 준비한 패턴을 순회하면서 치환합니다.
            msg = p.sub(lambda m: m.group(1) + "***", msg) if p.groups >= 2 else p.sub("***", msg)
        return msg  # 마스킹된 메시지를 반환합니다.


def get_logger(name="securenetops"):  # 공통 로거를 생성/재사용합니다.
    lvl = os.getenv("LOG_LEVEL", "INFO").upper()  # LOG_LEVEL 환경변수로 로그 레벨을 결정합니다.
    lg = logging.getLogger(name)  # 이름 기반 로거를 가져옵니다.
    if lg.handlers:  # 이미 핸들러가 있으면 중복 설정을 피하고 그대로 반환합니다.
        return lg
    lg.setLevel(lvl)  # 로거 레벨을 설정합니다.
    h = logging.StreamHandler()  # 표준 출력 스트림 핸들러를 생성합니다.
    extra = [os.getenv("CONTROLLER_API_TOKEN", "")]  # 토큰 값 자체도 마스킹 대상에 포함합니다.
    h.setFormatter(MaskingFormatter("%(asctime)s %(levelname)s %(name)s - %(message)s", extra))  # 커스텀 포매터를 연결합니다.
    lg.addHandler(h)  # 핸들러를 로거에 등록합니다.
    lg.propagate = False  # 상위 로거 전파를 막아 중복 출력 방지합니다.
    return lg  # 준비된 로거를 반환합니다.
