from src.core.logger import MaskingFormatter  # 로그 마스킹 포매터를 테스트합니다.
import logging  # 테스트용 LogRecord 생성을 위해 사용합니다.


def test_masking_formatter_masks_token():  # token 값이 마스킹되는지 확인합니다.
    f = MaskingFormatter("%(message)s", extra_secrets=["secret123"])
    r = logging.LogRecord("x", logging.INFO, __file__, 1, "token=secret123", args=(), exc_info=None)
    out = f.format(r)
    assert "***" in out and "secret123" not in out
