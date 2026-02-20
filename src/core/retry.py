from __future__ import annotations  # 파이썬 3.10+ 타입 힌트를 지연 평가합니다.
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type  # 재시도 정책 유틸을 가져옵니다.


def retryable(attempts: int = 3, min_s: float = 0.2, max_s: float = 2.0, exception_types=(Exception,)):  # 재사용 가능한 재시도 데코레이터 팩토리입니다.
    return retry(  # tenacity.retry 데코레이터 객체를 반환합니다.
        reraise=True,  # 마지막 시도까지 실패하면 예외를 다시 던집니다.
        stop=stop_after_attempt(attempts),  # 최대 시도 횟수를 제한합니다.
        wait=wait_exponential_jitter(initial=min_s, max=max_s),  # 지수 백오프 + 지터로 대기합니다.
        retry=retry_if_exception_type(exception_types),  # 지정한 예외 타입에서만 재시도합니다.
    )
