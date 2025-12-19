# Day04: Python netdiag (안전 진단)

## 목표
- 허용된 대상에 대해서만 DNS/TCP/HTTP 체크 수행(allowlist 관점)
- 결과를 JSON 리포트로 남기기

## 실행(컨테이너)
```bash
docker compose up -d --build
docker compose exec client bash
python -m tools.netdiag --targets configs/targets.yml --report reports/netdiag.json
cat reports/netdiag.json
```
