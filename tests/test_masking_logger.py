from src.core.logger import MaskingFormatter
import logging

def test_masking_formatter_masks_token():
    f = MaskingFormatter("%(message)s", extra_secrets=["secret123"])
    r = logging.LogRecord("x", logging.INFO, __file__, 1, "token=secret123", args=(), exc_info=None)
    out = f.format(r)
    assert "***" in out and "secret123" not in out
