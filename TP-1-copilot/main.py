from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path
import sys

# Try to import storage helpers from the tp2_task_manager sibling directory.
storage_dir = Path(__file__).resolve() / ".." / "tp2_task_manager"
storage_dir = storage_dir.resolve()
if storage_dir.exists():
	sys.path.insert(0, str(storage_dir))

try:
	from storage import load_tasks, save_tasks  # type: ignore
except Exception:
	def load_tasks(filename=None):
		return []

	def save_tasks(tasks, filename=None):
		return None


class Task(BaseModel):
	id: int
	title: str
	done: bool = False


class TaskCreate(BaseModel):
	title: str
	done: bool = False


app = FastAPI(title="Task Management API", version="1.0.0")

tasks_db: List[Task] = []
_task_id_counter = 1


@app.on_event("startup")
def _load_on_startup() -> None:
	global tasks_db, _task_id_counter
	raw = load_tasks(None)
	tasks_db = [Task(**t) for t in raw if isinstance(t, dict)]
	_task_id_counter = max((t.id for t in tasks_db), default=0) + 1


def _persist() -> None:
	save_tasks([t.dict() for t in tasks_db], None)


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
	_ensure_loaded()
	return tasks_db


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate):
	global _task_id_counter
	_ensure_loaded()
	task = Task(id=_task_id_counter, title=payload.title, done=payload.done)
	tasks_db.append(task)
	_task_id_counter += 1
	_persist()
	return task


@app.patch("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int):
	_ensure_loaded()
	for t in tasks_db:
		if t.id == task_id:
			t.done = not t.done
			_persist()
			return t
	raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
	_ensure_loaded()
	for i, t in enumerate(tasks_db):
		if t.id == task_id:
			tasks_db.pop(i)
			_persist()
			return {"message": "Task deleted"}
	raise HTTPException(status_code=404, detail="Task not found")


def _ensure_loaded() -> None:
	"""Ensure tasks_db is populated from persistent storage.

	This is used so tests that patch `load_tasks` (before creating the TestClient)
	will have their patched value honored when endpoints run.
	"""
	global tasks_db, _task_id_counter
	if not tasks_db:
		raw = load_tasks(None)
		tasks_db = [Task(**t) for t in raw if isinstance(t, dict)]
		_task_id_counter = max((t.id for t in tasks_db), default=0) + 1


__all__ = ["app", "load_tasks", "save_tasks"]
