import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient


def load_main_module():
    """Dynamically load the main.py module from the tp2-rest directory.

    Returns the loaded module object.
    """
    repo_dir = Path(__file__).resolve().parents[2]
    main_path = repo_dir / "main.py"
    spec = importlib.util.spec_from_file_location("rest_main", str(main_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_get_tasks_loads_from_storage():
    # Arrange: load module and patch load_tasks to return known data
    module = load_main_module()
    mock_tasks = [{"id": 1, "title": "Persisted Task", "done": False}]
    with patch.object(module, "load_tasks", return_value=mock_tasks):
        client = TestClient(module.app)
        # Act
        resp = client.get("/tasks")
        # Assert
        assert resp.status_code == 200
        assert resp.json() == mock_tasks


def test_create_task_calls_save():
    module = load_main_module()
    with patch.object(module, "load_tasks", return_value=[]):
        mock_save = MagicMock()
        with patch.object(module, "save_tasks", mock_save):
            client = TestClient(module.app)
            resp = client.post("/tasks", json={"title": "New via API"})

            assert resp.status_code == 201
            body = resp.json()
            assert body["id"] == 1
            assert body["title"] == "New via API"

            # save_tasks should have been called to persist new state
            assert mock_save.called
            args, kwargs = mock_save.call_args
            assert isinstance(args[0], list)
            assert any(t.get("title") == "New via API" for t in args[0])


def test_toggle_task_calls_save():
    module = load_main_module()
    initial = [{"id": 1, "title": "Toggler", "done": False}]
    with patch.object(module, "load_tasks", return_value=initial):
        mock_save = MagicMock()
        with patch.object(module, "save_tasks", mock_save):
            client = TestClient(module.app)
            resp = client.patch("/tasks/1/toggle")
            assert resp.status_code == 200
            body = resp.json()
            assert body["done"] is True
            assert mock_save.called


def test_delete_task_calls_save():
    module = load_main_module()
    initial = [{"id": 1, "title": "DeleteMe", "done": False}]
    with patch.object(module, "load_tasks", return_value=initial):
        mock_save = MagicMock()
        with patch.object(module, "save_tasks", mock_save):
            client = TestClient(module.app)
            resp = client.delete("/tasks/1")
            assert resp.status_code == 200
            assert resp.json().get("message") == "Task deleted"
            assert mock_save.called


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
