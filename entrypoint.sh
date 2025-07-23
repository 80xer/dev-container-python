#!/bin/sh

# 데이터베이스 테이블 초기화 (테이블이 없으면 생성)
python -c "from database import get_engine, create_table; engine = get_engine(); create_table(engine); engine.dispose()"

# rsyslog 서비스 시작 (cron 로그를 위해 필요)
rsyslogd

# cron 서비스 시작
cron -f &

# 컨테이너가 계속 실행되도록 로그 파일을 tail
tail -f /var/log/cron.log
