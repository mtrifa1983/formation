"""
Unit tests for Task Manager modules.
"""

import unittest
import os
import json
import tempfile
from typing import List, Dict, Any

# Test imports
try:
    from storage import Storage
    from cli import TaskManagerCLI
except ImportError:
    print("Warning: Could not import modules. Ensure you're running from the project directory.")


class TestStorage(unittest.TestCase):
    """Test cases for the Storage class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_tasks.json")
        self.storage = Storage(self.test_file)

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_load_empty_tasks(self) -> None:
        """Test loading tasks from a non-existent file."""
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])

    def test_add_task(self) -> None:
        """Test adding a task to storage."""
        task: Dict[str, Any] = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        }
        self.storage.add_task(task)
        tasks = self.storage.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Test Task")

    def test_update_task(self) -> None:
        """Test updating a task."""
        task: Dict[str, Any] = {
            "id": 1,
            "title": "Original Task",
            "description": "",
            "completed": False
        }
        self.storage.add_task(task)
        
        # Update the task
        result = self.storage.update_task(1, {"completed": True})
        self.assertTrue(result)
        
        # Verify the update
        tasks = self.storage.load_tasks()
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        task: Dict[str, Any] = {
            "id": 1,
            "title": "Task to Delete",
            "description": "",
            "completed": False
        }
        self.storage.add_task(task)
        
        # Delete the task
        result = self.storage.delete_task(1)
        self.assertTrue(result)
        
        # Verify deletion
        tasks = self.storage.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_nonexistent_task(self) -> None:
        """Test deleting a task that doesn't exist."""
        result = self.storage.delete_task(999)
        self.assertFalse(result)


class TestTaskManagerCLI(unittest.TestCase):
    """Test cases for the TaskManagerCLI class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_tasks.json")
        
        # Create CLI with test storage
        self.cli = TaskManagerCLI()
        self.cli.storage.filename = self.test_file

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_get_next_id_empty(self) -> None:
        """Test getting next ID when no tasks exist."""
        next_id = self.cli._get_next_id()
        self.assertEqual(next_id, 1)

    def test_get_next_id_with_tasks(self) -> None:
        """Test getting next ID when tasks exist."""
        task: Dict[str, Any] = {
            "id": 5,
            "title": "Task",
            "description": "",
            "completed": False
        }
        self.cli.storage.add_task(task)
        next_id = self.cli._get_next_id()
        self.assertEqual(next_id, 6)


def run_tests() -> None:
    """Run all unit tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManagerCLI))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    run_tests()
