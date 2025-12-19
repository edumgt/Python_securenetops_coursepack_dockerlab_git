# Day03: Git 운영 규칙(실무형)

## 목표
- 변경 이력/리뷰/롤백 가능한 운영 코드 만들기

## 권장 규칙
- 브랜치: main / dev / feature/* / hotfix/*
- 커밋 메시지: feat/fix/docs/refactor/test/chore
- 릴리즈: 태그로 버전 고정(day08 캡스톤에서 사용)

## 보안
- .env, token, password, key는 커밋 금지
- 민감정보는 로그에서도 마스킹(후반부 logger에서 적용)
