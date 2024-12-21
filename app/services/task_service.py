from sqlalchemy.orm import Session
from app.schemas import TaskCreateRequest
from app.models.task import TaskModel
import json


def create_task(db: Session, req: TaskCreateRequest) -> TaskModel:
    """
    user_goal, user_context を受け取り、DBに新規タスクを作成
    """
    # user_context を JSON 文字列化
    new_task = TaskModel(
        user_goal=req.user_goal,
        user_context=json.dumps(req.user_context)  # ここで変換
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
