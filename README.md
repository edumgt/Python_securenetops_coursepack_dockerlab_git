# SecureNetOps 과정 패키지 (Docker 네트워크 중심) - 8일 체크포인트

이 저장소는 8일 과정 커리큘럼에 맞춰 **Day01 ~ Day08**로 단계별 체크포인트(tag)를 제공합니다.
각 Day는 "강의자료(docs) + 과제(assignments) + 참고( solutions ) + 코드"로 구성되어 있습니다.

## 체크포인트 이동
```bash
git checkout day01   # 또는 day02~day08
```

## 추천 학습 흐름
- `docs/dayXX_*.md` : 강의/실습 진행서(학생용)
- `assignments/dayXX_tasks.md` : 과제(제출물/체크리스트)
- `solutions/dayXX_notes.md` : 강사용 해설/정답 방향(필요 시 공개)

## Day별 구성 요약
- Day01: 네트워크 기초 + 파이썬으로 DNS/TCP/HTTP 관측(로컬 실행)
- Day02: Docker 네트워크 랩 구성(고정 IP) + 서비스 구동
- Day03: GitHub(=Git) 운영 흐름/규칙 + 레포 표준화
- Day04: Python netdiag(안전 진단) + 리포트 JSON
- Day05: Intent-based(목적 중심) 상태 수렴 + HTTP client/리트라이
- Day06: Ansible 기초(도커 대상 운영 패턴 소개)
- Day07: Ansible 심화(roles/vault 구조 예시)
- Day08: Security audit + Monitoring agent + Tests + Capstone runbook

> 실습 중심이므로, Day02 이후는 Docker Compose 환경에서 진행합니다.
