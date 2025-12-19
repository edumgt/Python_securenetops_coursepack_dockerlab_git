# Day07: Ansible 심화(roles/vault 패턴)

## 목표
- roles로 재사용 가능한 운영 표준 만들기
- 민감정보는 vault로 관리(개념/패턴)

## 이 저장소 예시
- ansible/site.yml : roles 적용 엔트리
- ansible/roles/* : 역할별 작업 분리

## Vault 패턴(교육용 예시)
```bash
ansible-vault create ansible/group_vars/vault.yml
# vault.yml 안에 token/password 등을 넣고, site.yml에서 include_vars로 합치는 방식 권장
```
