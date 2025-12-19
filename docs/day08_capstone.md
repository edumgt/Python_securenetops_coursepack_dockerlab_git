# Day08: Capstone Runbook (통합 운영)

## 목표
- Git 태그(릴리즈) → Ansible(선택) → Python Intent 수렴 → 보안 점검 → 모니터링 → 테스트
- 결과물: runbook + JSON 리포트 3종

## 1) 기동
```bash
cp .env.example .env
docker compose up -d --build
```

## 2) 실행(클라이언트 컨테이너)
```bash
docker compose exec client bash
python -m tools.netdiag --report reports/netdiag.json
python -m tools.intent_apply --report reports/intent_report.json
python -m tools.security_audit --report reports/security_report.json
pytest -q
```

## 3) 모니터링 확인
```bash
docker compose logs -f monitor
# metrics: ./data/metrics.jsonl
```

## 4) 제출물(권장)
- docs/final_runbook.md (본인이 정리한 운영 절차/장애 대응)
- reports/netdiag.json
- reports/intent_report.json
- reports/security_report.json
- data/metrics.jsonl (일부 발췌)
