from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime, timezone


class TaskContent(BaseModel):
    action: str
    params: dict


class TaskResult(BaseModel):
    index: int
    output: Any
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskState(BaseModel):
    task_id: str
    contents: List[TaskContent]
    current_index: int
    results: List[TaskResult]
    execute_count: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # orm_mode を from_attributes に変更
    model_config = ConfigDict(from_attributes=True)


class TaskCreateRequest(BaseModel):
    user_goal: str
    user_context: Optional[dict] = Field(default_factory=dict)


class TaskCreateResponse(BaseModel):
    task_id: str


class TaskExecuteRequest(BaseModel):
    override_params: Optional[dict] = None


class TaskExecuteResponse(BaseModel):
    index: int
    success: bool
    output: Any


class TaskEvaluateRequest(BaseModel):
    results: List[TaskResult]
    user_goal: str
    context: dict = Field(default_factory=dict)


class TaskEvaluateResponse(BaseModel):
    ok: bool
    reason: Optional[str] = None


class TaskReplanRequest(BaseModel):
    current_contents: List[TaskContent]
    results: List[TaskResult]
    user_goal: str


class TaskReplanResponse(BaseModel):
    new_contents: List[TaskContent]


class TaskIndexUpdateRequest(BaseModel):
    new_index: int


class TaskCompleteResponse(BaseModel):
    message: str
