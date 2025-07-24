#!/bin/sh

# 1. DATABASE_URL 환경 변수가 있는지 확인
if [ -z "$DATABASE_URL" ]; then
  echo "Error: DATABASE_URL is not set." >&2
  exit 1
fi

# 2. cron 스케줄 파일에 환경 변수 동적 주입
#    - sed 명령어를 사용하여 /etc/cron.d/scheduler 파일의 맨 앞에 DATABASE_URL 선언을 추가합니다.
#    - 이렇게 하면 이 파일에 정의된 모든 cron 작업이 해당 변수를 사용할 수 있습니다.
sed -i "1iDATABASE_URL='$DATABASE_URL'\n" /etc/cron.d/scheduler

# 3. rsyslog 서비스 시작 (cron 로그를 위해 필요)
rsyslogd

# 4. cron 서비스 시작 (포그라운드에서 실행)
cron -f &

# 5. 컨테이너가 계속 실행되도록 로그 파일을 tail
tail -f /var/log/cron.log


