# Day05: Intent-based 상태 수렴

## 목표
- desired_state.yml에 정의된 상태로 controller_api가 수렴하도록 자동화
- 실패 시에도 리포트/원인 기록

## 실행
```bash
docker compose up -d --build
docker compose exec client bash
python -m tools.intent_apply --desired configs/desired_state.yml --report reports/intent_report.json
cat reports/intent_report.json
```

## 실습 포인트
- 토큰이 틀리면 403이 나와야 정상(인증/인가 확인)
- diff가 비어 있으면 "already converged"
