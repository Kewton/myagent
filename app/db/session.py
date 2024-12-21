from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 環境変数から読み込んだ接続文字列でEngineを作成
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPIのDependsで使用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
