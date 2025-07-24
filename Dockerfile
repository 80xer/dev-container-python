# Stage 1: Production Dependencies Builder
FROM python:3.11-slim as prod_deps_builder

WORKDIR /app
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Stage 2: Runner
FROM python:3.11-slim

WORKDIR /app

# 1. cron과 같은 시스템 패키지 설치 및 로그 파일 준비
RUN apt-get update && apt-get install -y cron rsyslog && \
    touch /var/log/cron.log

# Copy installed Python packages from the prod_deps_builder stage
COPY --from=prod_deps_builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 2. cron 스케줄 설정
COPY scheduler.cron /etc/cron.d/scheduler
RUN chmod 0644 /etc/cron.d/scheduler

# 3. 나머지 애플리케이션 코드 복사
COPY . .
# requirements-dev.txt는 운영 이미지에 포함되지 않도록 주의

# 4. 컨테이너 시작 시 cron 데몬과 로그를 함께 실행
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
