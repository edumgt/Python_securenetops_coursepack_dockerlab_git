from src.core.retry import retryable

def test_retryable_decorator_callable():
    dec = retryable(attempts=2)
    assert callable(dec)
