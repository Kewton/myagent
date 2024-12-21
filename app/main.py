from fastapi import FastAPI
from app.models.task import TaskModel
from app.db.session import engine
from app.db.base import Base
from app.api.v1 import common_endpoints
from app.api.v1 import task
from app.core.logger import setup_logging


setup_logging()

def create_tables():
    print("aaa")
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)

def get_application():
    app = FastAPI(
        title="My API",
        description="APIドキュメント",
        version="1.0.0",
        root_path="/api",
        swagger_ui_parameters={
            "docExpansion": "list",  # サイドバーにAPIリンクを表示
            "defaultModelsExpandDepth": -1  # モデルはサイドバーに表示しない
        }
    )
    create_tables()
    app.include_router(common_endpoints.router, prefix="/v1")
    app.include_router(task.router, prefix="/v1")
    return app


app = get_application()