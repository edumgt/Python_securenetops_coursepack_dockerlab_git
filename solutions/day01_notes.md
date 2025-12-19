# Day01 해설(강사용)

- DNS: socket.gethostbyname()는 /etc/hosts, DNS 설정 영향 받음
- TCP: create_connection()은 SYN/SYN-ACK 단계에서 막힐 수 있음(방화벽, 라우팅)
- HTTP: TLS/인증서/프록시 등 변수가 많으므로 실패 이유 문자열 기록이 중요
- 운영 습관: 타임아웃(짧게), 재시도(조건부), 로그/리포트 분리
