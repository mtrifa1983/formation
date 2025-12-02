from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Pydantic models
class Task(BaseModel):
    id: int
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str
    done: bool = False

app = FastAPI(title="Task Management API", version="1.0.0")

# In-memory storage (simple for demo)
tasks_db: List[Task] = []
_task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Return all tasks."""
    return tasks_db


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate):
    """Create a new task from the provided payload."""
    global _task_id_counter
    task = Task(id=_task_id_counter, title=payload.title, done=payload.done)
    tasks_db.append(task)
    _task_id_counter += 1
    return task


@app.patch("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(task_id: int):
    """Toggle the completion state of a task by id."""
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List
    from pathlib import Path
    import sys

    # Ensure we can import the existing tp2_task_manager storage module by
    # adding its directory to sys.path when running from this folder.
    storage_dir = Path(__file__).resolve().parents[2] / "tp2_task_manager"
    if storage_dir.exists():
        sys.path.insert(0, str(storage_dir))

    try:
        from storage import load_tasks, save_tasks
    except Exception:
        # Fallback: if import fails, provide no-op implementations to avoid runtime error
        def load_tasks(filename=None):
            return []

        def save_tasks(tasks, filename=None):
            return None


    # Pydantic models
    class Task(BaseModel):
        id: int
        title: str
        done: bool = False


    class TaskCreate(BaseModel):
        title: str
        done: bool = False


    app = FastAPI(title="Task Management API", version="1.0.0")

    # In-memory storage (backed by tp2_task_manager.storage persistence)
    tasks_db: List[Task] = []
    _task_id_counter = 1


    @app.on_event("startup")
    def _load_on_startup() -> None:
        """Load tasks from JSON storage into the in-memory database on startup."""
        global tasks_db, _task_id_counter
        raw = load_tasks(None)
        tasks_db = [Task(**t) for t in raw if isinstance(t, dict)]
        _task_id_counter = max((t.id for t in tasks_db), default=0) + 1


    def _persist() -> None:
        """Persist current in-memory tasks to JSON storage."""
        save_tasks([t.dict() for t in tasks_db], None)


    @app.get("/tasks", response_model=List[Task])
    async def get_tasks():
        """Return all tasks."""
        return tasks_db


    @app.post("/tasks", response_model=Task, status_code=201)
    async def create_task(payload: TaskCreate):
        """Create a new task from the provided payload and persist."""
        global _task_id_counter
        task = Task(id=_task_id_counter, title=payload.title, done=payload.done)
        tasks_db.append(task)
        _task_id_counter += 1
        _persist()
        return task


    @app.patch("/tasks/{task_id}/toggle", response_model=Task)
    async def toggle_task(task_id: int):
        """Toggle the completion state of a task by id and persist."""
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        from typing import List
        from pathlib import Path
        import sys

        # Try to import storage helpers from the tp2_task_manager package (sibling directory).
        storage_dir = Path(__file__).resolve().parents[2] / "tp2_task_manager"
        if storage_dir.exists():
            sys.path.insert(0, str(storage_dir))

        try:
            from storage import load_tasks, save_tasks  # type: ignore
        except Exception:
            # Fallback no-op implementations so the module can be imported in tests
            def load_tasks(filename=None):
                return []

            def save_tasks(tasks, filename=None):
                return None


        # Pydantic models
        class Task(BaseModel):
            id: int
            title: str
            done: bool = False


        class TaskCreate(BaseModel):
            title: str
            done: bool = False


        app = FastAPI(title="Task Management API", version="1.0.0")

        # In-memory storage (backed by tp2_task_manager.storage persistence)
        tasks_db: List[Task] = []
        _task_id_counter = 1


        @app.on_event("startup")
        def _load_on_startup() -> None:
            """Load tasks from JSON storage into the in-memory database on startup."""
            global tasks_db, _task_id_counter
            raw = load_tasks(None)
            tasks_db = [Task(**t) for t in raw if isinstance(t, dict)]
            _task_id_counter = max((t.id for t in tasks_db), default=0) + 1


        def _persist() -> None:
            """Persist current in-memory tasks to JSON storage."""
            save_tasks([t.dict() for t in tasks_db], None)


        @app.get("/tasks", response_model=List[Task])
        async def get_tasks():
            """Return all tasks."""
            return tasks_db


        @app.post("/tasks", response_model=Task, status_code=201)
        async def create_task(payload: TaskCreate):
            """Create a new task from the provided payload and persist."""
            global _task_id_counter
            task = Task(id=_task_id_counter, title=payload.title, done=payload.done)
            tasks_db.append(task)
            _task_id_counter += 1
            _persist()
            return task


        @app.patch("/tasks/{task_id}/toggle", response_model=Task)
        async def toggle_task(task_id: int):
            """Toggle the completion state of a task by id and persist."""
            for t in tasks_db:
                if t.id == task_id:
                    t.done = not t.done
                    _persist()
                    return t
            raise HTTPException(status_code=404, detail="Task not found")


        @app.delete("/tasks/{task_id}")
        async def delete_task(task_id: int):
            """Delete a task by id and persist."""
            for i, t in enumerate(tasks_db):
                if t.id == task_id:
                    tasks_db.pop(i)
                    _persist()
                    return {"message": "Task deleted"}
            raise HTTPException(status_code=404, detail="Task not found")


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="0.0.0.0", port=8000)
