# Day06: Ansible 기초(도커 랩 대상)

컨테이너는 기본적으로 SSH 서버가 없으므로, Day06에서는 다음 중 하나로 실습합니다.

1) **로컬에서 Docker를 제어**하는 방식(권장): community.docker 컬렉션을 사용
2) (선택) 컨테이너에 SSH를 올리는 방식(교육 난이도 상승)

여기서는 1) 방식을 예시로 제공합니다.
- 대상: target_web 컨테이너에 파일/환경 설정 적용(예: 설정 파일 배포, 재시작)

## 준비(로컬)
```bash
pip install ansible
ansible-galaxy collection install community.docker
```

## 실행 예시
```bash
cd ansible
ansible-playbook -i inventory.ini playbooks/copy_banner.yml
```
