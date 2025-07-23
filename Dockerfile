FROM python:3.11-slim

WORKDIR /app

# 1. cron과 같은 시스템 패키지 설치 및 로그 파일 준비
RUN apt-get update && apt-get install -y cron rsyslog && \
    touch /var/log/cron.log

# 2. 파이썬 의존성 설치를 위해 requirements.txt 먼저 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. cron 스케줄 설정
COPY scheduler.cron /etc/cron.d/scheduler
RUN chmod 0644 /etc/cron.d/scheduler && \
    crontab /etc/cron.d/scheduler

# 4. 나머지 애플리케이션 코드 복사
COPY . .

# 5. 컨테이너 시작 시 cron 데몬과 로그를 함께 실행
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
