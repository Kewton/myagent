# my_fastapi_project/app/tests/test_task.py

import pytest
from fastapi.testclient import TestClient
from app.main import app  # FastAPI アプリのエントリーポイントをインポート

client = TestClient(app)


@pytest.mark.parametrize("user_goal,user_context", [
    ("メールに添付されたPDFを要約して上司に送付", {}),
    ("シンプルなTODOリスト作成", {"urgency": "high"}),
])
def test_create_task(user_goal, user_context):
    """
    /task/create エンドポイントのテスト
    """
    print(f"test_create_task start for user_goal: {user_goal}")
    payload = {
        "user_goal": user_goal,
        "user_context": user_context
    }
    response = client.post("/api/v1/task/create", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    print(f"Response: {json_data}")
    assert "task_id" in json_data  # 戻り値に task_id が含まれているか


def test_get_task_state():
    """
    /task/{task_id} (GET) テスト
    """
    task_id = "dummy_task_id"
    response = client.get(f"/api/v1/task/{task_id}")
    assert response.status_code == 200
    json_data = response.json()
    # TaskState のレスポンスフォーマットを簡易チェック
    assert json_data["task_id"] == task_id
    assert isinstance(json_data["contents"], list)
    assert "results" in json_data
    assert "execute_count" in json_data


def test_execute_task():
    """
    /task/{task_id}/execute (POST) テスト
    """
    task_id = "dummy_task_id"
    payload = {
        "override_params": {"sample_key": "sample_value"}
    }
    response = client.post(f"/api/v1/task/{task_id}/execute", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    # TaskExecuteResponse のレスポンスフォーマットを簡易チェック
    assert "index" in json_data
    assert "success" in json_data
    assert "output" in json_data


def test_evaluate_task():
    """
    /task/{task_id}/evaluate (POST) テスト
    """
    task_id = "dummy_task_id"
    payload = {
        "results": [
            {
                "index": 0,
                "output": {"msg": "Execution Done"},
                "timestamp": "2023-10-01T12:00:00"
            }
        ],
        "user_goal": "PDFを要約してメール送付",
        "context": {}
    }
    response = client.post(f"/api/v1/task/{task_id}/evaluate", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    # TaskEvaluateResponse のレスポンスをチェック
    assert "ok" in json_data
    assert "reason" in json_data or json_data["reason"] is None


def test_replan_task():
    """
    /task/{task_id}/replan (POST) テスト
    """
    task_id = "dummy_task_id"
    payload = {
        "current_contents": [
            {"action": "get_pdf", "params": {}}
        ],
        "results": [
            {
                "index": 0,
                "output": {"msg": "Execution Done"},
                "timestamp": "2023-10-01T12:00:00"
            }
        ],
        "user_goal": "PDFを要約してメール送付"
    }
    response = client.post(f"/api/v1/task/{task_id}/replan", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    # TaskReplanResponse のレスポンスをチェック
    assert "new_contents" in json_data
    assert isinstance(json_data["new_contents"], list)


def test_update_task_index():
    """
    /task/{task_id}/index (PUT) テスト
    """
    task_id = "dummy_task_id"
    payload = {
        "new_index": 1
    }
    response = client.put(f"/api/v1/task/{task_id}/index", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    # メッセージのみ返すシンプルな実装を想定
    assert "message" in json_data
    assert "Index updated to 1" in json_data["message"]


def test_complete_task():
    """
    /task/{task_id}/complete (PUT) テスト
    """
    task_id = "dummy_task_id"
    response = client.put(f"/api/v1/task/{task_id}/complete")
    assert response.status_code == 200
    json_data = response.json()
    # TaskCompleteResponse
    assert "message" in json_data
    assert f"Task {task_id} completed." in json_data["message"]
