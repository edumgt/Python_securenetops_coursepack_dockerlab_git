# Day01: 네트워크 기초 + Python 관측

## 목표
- DNS / TCP 연결 / HTTP 요청이 실제로 어떻게 동작하는지 "운영자 관점"으로 관측
- 타임아웃, 예외처리, 결과 표준화(JSON) 습관 잡기

## 실습 1) 로컬에서 기본 진단 명령(참고)
- ping, traceroute, nslookup/dig, curl, ss/netstat

## 실습 2) Python으로 DNS/TCP/HTTP 관측
```bash
python tools/net_basics.py --host example.com --port 443 --url https://example.com
python tools/net_basics.py --host localhost --port 80 --url http://localhost
```

## 체크 포인트
- 타임아웃이 없으면 운영 코드가 "멈춤" 상태가 될 수 있습니다.
- 실패를 예외로만 끝내지 말고 **리포트 형태**로 남겨야 합니다.
