import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.exc import IntegrityError

# 환경 변수에서 DATABASE_URL을 읽어오거나, 기본값으로 SQLite 사용
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///quotes.db")

metadata = MetaData()

quotes_table = Table(
    "quotes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quote", String, unique=True, nullable=False),
    Column("author", String, nullable=False),
)

def get_engine(db_url=None):
    """
    SQLAlchemy 엔진을 반환합니다. 테스트 시에는 db_url을 인자로 받아 사용합니다.
    """
    if db_url is None:
        db_url = DATABASE_URL
    return create_engine(db_url)

def create_table(engine):
    """
    데이터베이스에 테이블을 생성합니다. 이미 존재하면 생성하지 않습니다.
    """
    metadata.create_all(engine)

def save_quote(engine, quote, author):
    """
    명언을 데이터베이스에 저장합니다.
    """
    conn = engine.connect()
    try:
        ins = quotes_table.insert().values(quote=quote, author=author)
        conn.execute(ins)
        conn.commit()
        return True
    except IntegrityError:
        # Unique 제약 조건 위반 (이미 존재하는 명언)
        conn.rollback()
        return False
    finally:
        conn.close()
