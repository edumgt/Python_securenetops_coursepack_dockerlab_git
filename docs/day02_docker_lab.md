# Day02: Docker 네트워크 랩 구성

## 목표
- 고정 IP 기반 Docker 네트워크 랩 구성
- controller_api(모의 컨트롤러) / target_web(대상) / client(실습) / monitor(관측) 실행

## 실행
```bash
cp .env.example .env
docker compose up -d --build
docker compose ps
```

## 확인
```bash
curl http://localhost:8000/health
curl http://localhost:8080/health
docker compose exec client bash
```

## 네트워크(고정 IP)
- controller_api: 172.30.0.10:8000
- target_web:     172.30.0.20:8080
- monitor:        172.30.0.30
- client:         172.30.0.40
