"""
Storage Module - Handles task persistence

This module provides the Storage class for saving and loading tasks
from a JSON file.
"""

import json
import os
from typing import List, Dict, Any, Optional


class Storage:
    """Handles storage of tasks in a JSON file."""

    def __init__(self, filename: str = "tasks.json") -> None:
        """
        Initialize the Storage instance.

        Args:
            filename: The name of the file to store tasks.
        """
        self.filename = filename

    def load_tasks(self) -> List[Dict[str, Any]]:
        """
        Load tasks from the storage file.

        Returns:
            A list of task dictionaries. Returns an empty list if file doesn't exist.
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                return tasks if isinstance(tasks, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """
        Save tasks to the storage file.

        Args:
            tasks: A list of task dictionaries to save.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)

    def add_task(self, task: Dict[str, Any]) -> None:
        """
        Add a new task to storage.

        Args:
            task: The task dictionary to add.
        """
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if task was deleted, False otherwise.
        """
        tasks = self.load_tasks()
        original_length = len(tasks)
        tasks = [task for task in tasks if task.get("id") != task_id]

        if len(tasks) < original_length:
            self.save_tasks(tasks)
            return True
        return False

    def update_task(self, task_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update a task by its ID.

        Args:
            task_id: The ID of the task to update.
            updates: Dictionary of fields to update.

        Returns:
            True if task was updated, False otherwise.
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                task.update(updates)
                self.save_tasks(tasks)
                return True
        return False


# Module-level convenience functions
DEFAULT_TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks(filename: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load tasks from a JSON file.

    This convenience function wraps :class:`Storage.load_tasks` and uses a
    default file `tasks.json` located next to this module when no filename is
    provided. If the file does not exist, an empty list is returned.

    Parameters
    ----------
    filename:
        Optional path to the JSON file. If ``None`` the module default is used.

    Returns
    -------
    list[dict]
        The list of tasks loaded from disk (empty list if file missing or
        invalid).

    Examples
    --------
    >>> # load from default file
    >>> tasks = load_tasks()
    >>> isinstance(tasks, list)
    True
    """
    file = filename or DEFAULT_TASKS_FILE
    storage = Storage(file)
    return storage.load_tasks()


def save_tasks(tasks: List[Dict[str, Any]], filename: Optional[str] = None) -> None:
    """Save tasks to a JSON file.

    This convenience function wraps :class:`Storage.save_tasks` and writes to
    the module default `tasks.json` when no filename is provided.

    Parameters
    ----------
    tasks:
        List of task dictionaries to persist.
    filename:
        Optional path to the JSON file. If ``None`` the module default is used.

    Examples
    --------
    >>> save_tasks([{"id":1, "title":"Test", "completed":False}])
    """
    file = filename or DEFAULT_TASKS_FILE
    storage = Storage(file)
    # Ensure we propagate IO errors to the caller so failures are visible
    storage.save_tasks(tasks)
