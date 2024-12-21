from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import List
from app.schemas import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskState,
    TaskExecuteRequest,
    TaskExecuteResponse,
    TaskEvaluateRequest,
    TaskEvaluateResponse,
    TaskReplanRequest,
    TaskReplanResponse,
    TaskIndexUpdateRequest,
    TaskCompleteResponse,
)
from app.core.logger import writedebuglog, writeinfolog, declogger
from app.services.task_service import create_task as service_create_task

# 例： DB セッションやサービスクラスなどを DI(Depend on) するための Depends
# from app.services.task_service import TaskService
# from app.db.session import get_db

router = APIRouter()


@router.post("/task/create", response_model=TaskCreateResponse)
def create_task(
    req: TaskCreateRequest,
    db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskCreateResponse:
    """
    ユーザの要求 (user_goal, user_context) を受け取り、
    タスクを新規生成して TaskID を返す。
    """
    # TODO: 実際のビジネスロジックでタスク分割 (LLM / ルールベース など)
    # task_state = task_service.create_task(req)
    #writeinfolog(req)
    #dummy_task_id = "task_1234"
    #return TaskCreateResponse(task_id=dummy_task_id)
    print("##### 1")
    task_obj = service_create_task(db, req)
    print("##### 2")
    return TaskCreateResponse(task_id=task_obj.id)

@router.get("/task/{task_id}", response_model=TaskState)
def get_task_state(
    task_id: str,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskState:
    """
    タスクの現在の状態 (contents, current_index, results, 実行回数等) を返す。
    """
    # task_state = task_service.get_task_state(task_id)
    dummy_state = TaskState(
        task_id=task_id,
        contents=[],
        current_index=0,
        results=[],
        execute_count=0
    )
    return dummy_state


@router.post("/task/{task_id}/execute", response_model=TaskExecuteResponse)
def execute_task(
    task_id: str,
    req: TaskExecuteRequest,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskExecuteResponse:
    """
    current_index に対応するタスクを実行し、その結果を返す。
    実行結果(成功/失敗, 出力など)を TaskState に記録。
    """
    # result = task_service.execute_task(task_id, req.override_params)
    dummy_result = TaskExecuteResponse(
        index=0,
        success=True,
        output={"msg": "Execution Done"}
    )
    return dummy_result


@router.post("/task/{task_id}/evaluate", response_model=TaskEvaluateResponse)
def evaluate_task(
    task_id: str,
    req: TaskEvaluateRequest,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskEvaluateResponse:
    """
    直近の実行結果を LLM 等で評価し、OK/NG を返す。
    """
    # eval_result = task_service.evaluate_task(task_id, req)
    dummy_eval_result = TaskEvaluateResponse(ok=True, reason="Looks good.")
    return dummy_eval_result


@router.post("/task/{task_id}/replan", response_model=TaskReplanResponse)
def replan_task(
    task_id: str,
    req: TaskReplanRequest,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskReplanResponse:
    """
    実行結果が NG の場合などに、タスクを再計画 (タスクリスト再構成) する。
    """
    # new_contents = task_service.replan_task(task_id, req)
    dummy_replan = TaskReplanResponse(new_contents=[])
    return dummy_replan


@router.put("/task/{task_id}/index")
def update_task_index(
    task_id: str,
    req: TaskIndexUpdateRequest,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
):
    """
    タスクの current_index を更新する。
    """
    # task_service.update_task_index(task_id, req.new_index)
    return {"message": "Index updated to {}".format(req.new_index)}


@router.put("/task/{task_id}/complete", response_model=TaskCompleteResponse)
def complete_task(
    task_id: str,
    # db: Session = Depends(get_db),
    # task_service: TaskService = Depends()
) -> TaskCompleteResponse:
    """
    タスクを完了状態にし、必要なら通知やメモリ更新を行う。
    """
    # task_service.complete_task(task_id)
    return TaskCompleteResponse(message=f"Task {task_id} completed.")
