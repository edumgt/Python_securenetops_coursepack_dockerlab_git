# SecureNetOps 과정 패키지 (Docker 네트워크 중심) - 8일 체크포인트

이 저장소는 8일 과정 커리큘럼에 맞춰 **Day01 ~ Day08**로 단계별 체크포인트(tag)를 제공합니다.
각 Day는 "강의자료(docs) + 과제(assignments) + 참고(solutions) + 코드"로 구성되어 있습니다.

## WSL(Windows Subsystem for Linux) 기반 사용 가이드

1. **WSL2 설치 및 Ubuntu 준비**
   - PowerShell(관리자)에서 `wsl --install` 실행
   - 재부팅 후 Ubuntu 초기 사용자 생성

2. **프로젝트 클론(WSL 내부 경로 권장)**
   - 성능/권한 문제를 줄이기 위해 `/home/<user>/...` 경로에 클론
   - 예시:
     ```bash
     cd ~
     git clone <REPO_URL>
     cd Python_securenetops_coursepack_dockerlab_git
     ```

3. **Python 및 의존성 설치**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Docker Desktop + WSL 연동**
   - Docker Desktop 설치 후 **Settings → Resources → WSL integration**에서 배포판 활성화
   - 확인:
     ```bash
     docker compose version
     ```

5. **Day 체크포인트 이동(WSL 대응 스크립트)**
   ```bash
   bash scripts/checkout_day.sh day01
   ```

## 체크포인트 이동 (직접)
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
