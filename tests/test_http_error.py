from src.core.http import HttpError

def test_http_error_fields():
    e = HttpError("x", status_code=401, payload={"detail":"no"})
    assert e.status_code == 401
    assert e.payload["detail"] == "no"
