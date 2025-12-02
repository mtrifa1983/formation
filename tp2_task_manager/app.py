"""
Task Manager Application - Main Module

Provides Task domain model and TaskService for CRUD operations with persistence.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional

from storage import load_tasks, save_tasks


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID cannot be found."""
    pass


@dataclass
class Task:
    """Simple Task data structure.

    Attributes
    ----------
    id : int
        Unique identifier for the task.
    title : str
        Short human-readable title.
    done : bool
        Completion flag (default False).

    Examples
    --------
    >>> t = Task(id=1, title='Buy milk')
    >>> t.done
    False
    >>> asdict(t)
    {'id': 1, 'title': 'Buy milk', 'done': False}
    """

    id: int
    title: str
    done: bool = False


class TaskRepository:
    """Internal repository layer managing in-memory task storage.
    
    This class handles the conversion between Task objects and raw data,
    enforcing the single responsibility of managing in-memory state.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add(self, task: Task) -> None:
        """Add a task to the repository.
        
        Parameters
        ----------
        task : Task
            The task object to add.
        """
        self._tasks.append(task)
        self._next_id = max(t.id for t in self._tasks) + 1 if self._tasks else 1

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by ID.
        
        Parameters
        ----------
        task_id : int
            The task ID to search for.
            
        Returns
        -------
        Task or None
            The Task object if found, None otherwise.
        """
        return next((t for t in self._tasks if t.id == task_id), None)

    def find_all(self) -> List[Task]:
        """Get all tasks.
        
        Returns
        -------
        list[Task]
            A shallow copy of all tasks.
        """
        return list(self._tasks)

    def remove_by_id(self, task_id: int) -> bool:
        """Remove a task by ID.
        
        Parameters
        ----------
        task_id : int
            The task ID to remove.
            
        Returns
        -------
        bool
            True if task was removed, False if not found.
        """
        original_count = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        return len(self._tasks) < original_count

    def get_next_id(self) -> int:
        """Get the next available ID.
        
        Returns
        -------
        int
            The next ID to assign to a new task.
        """
        return self._next_id

    def load_from_dicts(self, task_dicts: List[dict]) -> None:
        """Load tasks from dictionary representation.
        
        Parameters
        ----------
        task_dicts : list[dict]
            List of dictionaries with id, title, done keys.
        """
        self._tasks = [
            Task(**{k: v for k, v in t.items() if k in {"id", "title", "done"}})
            for t in task_dicts
        ]
        self._next_id = max(t.id for t in self._tasks) + 1 if self._tasks else 1

    def to_dicts(self) -> List[dict]:
        """Convert tasks to dictionary representation.
        
        Returns
        -------
        list[dict]
            List of task dictionaries suitable for JSON serialization.
        """
        return [asdict(t) for t in self._tasks]


class TaskService:
    """Service layer for task management with persistence.

    Provides CRUD operations with automatic persistence to JSON storage.
    Tasks are represented internally as Task dataclasses but persisted as
    dictionaries. This class coordinates between the repository (in-memory
    state) and storage (persistence layer).

    Parameters
    ----------
    filename : str, optional
        Path to the JSON file for persistence. If None, the storage module
        default is used.

    Examples
    --------
    >>> svc = TaskService()
    >>> task = svc.create_task('Write tests')
    >>> task.id
    1
    >>> all_tasks = svc.retrieve_all_tasks()
    >>> svc.update_task_completion(1)
    >>> svc.delete_task(1)
    """

    def __init__(self, filename: Optional[str] = None) -> None:
        """Initialize the service and load persisted tasks.

        Parameters
        ----------
        filename : str, optional
            Optional path to the JSON file. When None, the storage module
            default is used.
        """
        self._filename = filename
        self._repository = TaskRepository()
        self._sync_from_storage()

    def _sync_from_storage(self) -> None:
        """Load tasks from persistent storage into the repository.
        
        Private method handling the synchronization between storage and
        in-memory repository.
        """
        raw_tasks = load_tasks(self._filename)
        self._repository.load_from_dicts(raw_tasks)

    def _sync_to_storage(self) -> None:
        """Persist repository state to storage.
        
        Private method handling the synchronization between in-memory
        repository and persistent storage.
        """
        task_dicts = self._repository.to_dicts()
        save_tasks(task_dicts, self._filename)

    def create_task(self, title: str) -> Task:
        """Create a new task and persist it.

        Parameters
        ----------
        title : str
            The task title.

        Returns
        -------
        Task
            The newly created Task object with assigned ID.
            
        Raises
        ------
        ValueError
            If title is empty or None.
            
        Examples
        --------
        >>> task = service.create_task('Buy milk')
        >>> task.title
        'Buy milk'
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(id=self._repository.get_next_id(), title=title.strip())
        self._repository.add(task)
        self._sync_to_storage()
        return task

    def retrieve_all_tasks(self) -> List[Task]:
        """Retrieve all tasks, with fresh data from storage.

        Returns
        -------
        list[Task]
            List of all tasks in the system.
            
        Examples
        --------
        >>> tasks = service.retrieve_all_tasks()
        >>> len(tasks)
        3
        """
        # Reload to ensure consistency with other processes
        self._sync_from_storage()
        return self._repository.find_all()

    def retrieve_task_by_id(self, task_id: int) -> Task:
        """Retrieve a single task by ID.

        Parameters
        ----------
        task_id : int
            The ID of the task to retrieve.

        Returns
        -------
        Task
            The requested task object.
            
        Raises
        ------
        TaskNotFoundError
            If no task with the given ID exists.
            
        Examples
        --------
        >>> task = service.retrieve_task_by_id(1)
        >>> task.title
        'Buy milk'
        """
        task = self._repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def update_task_completion(self, task_id: int) -> Task:
        """Toggle the completion status of a task.

        Parameters
        ----------
        task_id : int
            The ID of the task to toggle.

        Returns
        -------
        Task
            The updated task object.
            
        Raises
        ------
        TaskNotFoundError
            If no task with the given ID exists.
            
        Examples
        --------
        >>> task = service.update_task_completion(1)
        >>> task.done
        True
        """
        task = self._repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        task.done = not task.done
        self._sync_to_storage()
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Parameters
        ----------
        task_id : int
            The ID of the task to delete.

        Raises
        ------
        TaskNotFoundError
            If no task with the given ID exists.
            
        Examples
        --------
        >>> service.delete_task(1)
        """
        if not self._repository.remove_by_id(task_id):
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        self._sync_to_storage()



