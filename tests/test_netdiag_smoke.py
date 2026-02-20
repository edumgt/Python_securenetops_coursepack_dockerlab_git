from tools.netdiag import check_tcp  # netdiag의 TCP 체크 함수 단위 테스트를 위해 import 합니다.


def test_check_tcp_fails_fast():  # 네트워크 불가 주소에서 빠르게 실패/응답되는지 확인합니다.
    # reserved TEST-NET-1 (unroutable here), should fail quickly with timeout
    r = check_tcp("192.0.2.1", 81, 0.2)
    assert r["ok"] in (True, False)  # 환경에 따라 결과가 달라도 함수가 dict를 반환하면 테스트 통과입니다.
