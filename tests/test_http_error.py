from src.core.http import HttpError  # HttpError 속성 저장 동작을 검증하기 위해 import 합니다.


def test_http_error_fields():  # status_code/payload 필드가 정상 저장되는지 확인합니다.
    e = HttpError("x", status_code=401, payload={"detail": "no"})
    assert e.status_code == 401
    assert e.payload["detail"] == "no"
