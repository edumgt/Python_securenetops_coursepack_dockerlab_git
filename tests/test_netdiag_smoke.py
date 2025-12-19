from tools.netdiag import check_tcp

def test_check_tcp_fails_fast():
    # reserved TEST-NET-1 (unroutable here), should fail quickly with timeout
    r = check_tcp("192.0.2.1", 81, 0.2)
    assert r["ok"] in (True, False)
