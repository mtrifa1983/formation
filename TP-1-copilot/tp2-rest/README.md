# Task Management API (FastAPI)

This folder provides a small FastAPI application to manage tasks (in-memory demo).

Endpoints
- GET /tasks -> list all tasks
- POST /tasks -> create a task (body: {"title": "...", "done": false})
- PATCH /tasks/{id}/toggle -> toggle completion
- DELETE /tasks/{id} -> delete task

Run locally (after installing dependencies)

Windows (PowerShell):

```powershell
# Install dependencies
python -m pip install -r requirements.txt

# Run with uvicorn
python main.py
# or
uvicorn main:app --reload --port 8000
```

Quick test with curl

```powershell
# Create
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
# List
curl http://127.0.0.1:8000/tasks
# Toggle
curl -X PATCH http://127.0.0.1:8000/tasks/1/toggle
# Delete
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

Notes
- This example uses in-memory storage. For persistence, replace `tasks_db` with your storage layer (file/DB) and wire in your service layer.
- The included `requirements.txt` lists `fastapi` and `uvicorn`.
