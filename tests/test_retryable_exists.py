from src.core.retry import retryable  # 재시도 데코레이터 팩토리를 import 합니다.


def test_retryable_decorator_callable():  # retryable()이 callable 데코레이터를 반환하는지 확인합니다.
    dec = retryable(attempts=2)
    assert callable(dec)
