import pytest
import os
import sys

# Add the project root to the Python path to allow imports from 'scripts' and 'database'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.scrape_quotes import run_scraping_task
from database import get_engine, create_table, quotes_table, MetaData

# 테스트용 데이터베이스 파일 경로
TEST_DB_URL = "sqlite:///test_quotes.db"
TEST_DB_FILE = "test_quotes.db"

@pytest.fixture
def db_engine(monkeypatch):
    """
    테스트를 위한 격리된 SQLAlchemy 엔진을 생성하고, 테스트 후 정리합니다.
    """
    # 1. 테스트용 DB 파일 경로 설정 및 기존 파일 삭제
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    # 2. 테스트용 엔진 생성
    engine = get_engine(TEST_DB_URL)

    # 3. 스크립트가 DB에 연결할 때 테스트용 엔진을 사용하도록 설정
    monkeypatch.setattr('scripts.scrape_quotes.get_engine', lambda: engine)

    # 4. 테스트에서 사용할 테이블 생성
    create_table(engine)

    # 5. 테스트 함수에 엔진 객체를 넘겨줌
    yield engine

    # 6. 테스트 종료 후 엔진 닫고 파일 삭제
    engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

def test_run_scraping_task_saves_data(db_engine):
    """
    run_scraping_task 함수가 웹에서 명언을 스크레이핑하여
    테스트 데이터베이스에 성공적으로 저장하는지 검증합니다.
    """
    # Given: 격리된 DB 엔진이 준비된 상태 (by fixture)

    # When: 핵심 로직 함수를 실행
    saved_count = run_scraping_task()

    # Then: 결과 검증
    assert saved_count > 0

    # Fixture로부터 받은 엔진을 사용하여 결과 확인
    with db_engine.connect() as conn:
        result = conn.execute(quotes_table.select()).fetchall()
        quotes = [row._asdict() for row in result] # SQLAlchemy Row 객체를 딕셔너리로 변환

    assert len(quotes) == saved_count
    assert 'author' in quotes[0]
    assert 'quote' in quotes[0]
    print(f"\nSuccessfully verified that {len(quotes)} quotes were saved to the test database.")
