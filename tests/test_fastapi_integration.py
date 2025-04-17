import pytest
from fastapi.testclient import TestClient
from server import app, get_todo

client = TestClient(app)

def test_get_todo_endpoint():
    """Test dell'endpoint /todo/{item_id}"""
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "task": "Task 1"}

def test_get_todo_invalid_id():
    """Test dell'endpoint con ID non valido"""
    response = client.get("/todo/abc")
    assert response.status_code == 422  # FastAPI restituisce 422 per errori di validazione

@pytest.mark.asyncio
async def test_get_todo_tool():
    """Test del tool MCP get_todo_tool"""
    result = await get_todo(1)
    assert result == {"id": 1, "task": "Task 1"}

def test_fastapi_app_initialization():
    """Test dell'inizializzazione dell'app FastAPI"""
    assert app is not None
    assert app.title == "FastAPI" 