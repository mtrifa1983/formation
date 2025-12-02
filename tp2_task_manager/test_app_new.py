"""
Unit tests for Task Manager application using pytest and mocks.

Tests cover the Task domain model, TaskRepository, and TaskService layers
with mocked storage to isolate business logic.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from app import Task, TaskService, TaskRepository, TaskNotFoundError
from storage import Storage


class TestTask:
    """Tests for Task dataclass."""

    def test_task_creation_with_defaults(self) -> None:
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.done is False

    def test_task_creation_with_done(self) -> None:
        """Test creating a task with done=True."""
        task = Task(id=1, title="Done Task", done=True)
        assert task.done is True

    def test_task_equality(self) -> None:
        """Test task equality comparison."""
        task1 = Task(id=1, title="Test", done=False)
        task2 = Task(id=1, title="Test", done=False)
        assert task1 == task2


class TestTaskRepository:
    """Tests for TaskRepository layer."""

    @pytest.fixture
    def repo(self) -> TaskRepository:
        """Create a fresh repository for each test."""
        return TaskRepository()

    def test_add_task(self, repo: TaskRepository) -> None:
        """Test adding a task to repository."""
        task = Task(id=1, title="Test")
        repo.add(task)
        assert len(repo.find_all()) == 1

    def test_find_by_id_existing(self, repo: TaskRepository) -> None:
        """Test finding an existing task."""
        task = Task(id=1, title="Test")
        repo.add(task)
        found = repo.find_by_id(1)
        assert found is not None
        assert found.title == "Test"

    def test_find_by_id_missing(self, repo: TaskRepository) -> None:
        """Test finding a non-existent task returns None."""
        result = repo.find_by_id(999)
        assert result is None

    def test_remove_by_id_existing(self, repo: TaskRepository) -> None:
        """Test removing an existing task."""
        task = Task(id=1, title="Test")
        repo.add(task)
        result = repo.remove_by_id(1)
        assert result is True
        assert len(repo.find_all()) == 0

    def test_remove_by_id_missing(self, repo: TaskRepository) -> None:
        """Test removing a non-existent task."""
        result = repo.remove_by_id(999)
        assert result is False

    def test_get_next_id(self, repo: TaskRepository) -> None:
        """Test next ID generation."""
        assert repo.get_next_id() == 1
        task = Task(id=1, title="Test")
        repo.add(task)
        assert repo.get_next_id() == 2

    def test_get_next_id_with_gaps(self, repo: TaskRepository) -> None:
        """Test next ID generation with gaps in IDs."""
        repo.add(Task(id=1, title="Task 1"))
        repo.add(Task(id=3, title="Task 3"))
        repo.add(Task(id=5, title="Task 5"))
        assert repo.get_next_id() == 6

    def test_load_from_dicts(self, repo: TaskRepository) -> None:
        """Test loading tasks from dictionary representation."""
        dicts = [
            {"id": 1, "title": "Task 1", "done": False},
            {"id": 2, "title": "Task 2", "done": True},
        ]
        repo.load_from_dicts(dicts)
        tasks = repo.find_all()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].done is True

    def test_load_from_dicts_ignores_extra_fields(self, repo: TaskRepository) -> None:
        """Test that load_from_dicts ignores extra fields."""
        dicts = [
            {"id": 1, "title": "Task", "done": False, "extra": "ignored", "another": 123},
        ]
        repo.load_from_dicts(dicts)
        tasks = repo.find_all()
        assert len(tasks) == 1
        assert tasks[0].title == "Task"

    def test_to_dicts(self, repo: TaskRepository) -> None:
        """Test converting tasks to dictionary representation."""
        task = Task(id=1, title="Test", done=False)
        repo.add(task)
        dicts = repo.to_dicts()
        assert len(dicts) == 1
        assert dicts[0]["title"] == "Test"
        assert dicts[0]["done"] is False

    def test_find_all_returns_copy(self, repo: TaskRepository) -> None:
        """Test that find_all returns a shallow copy, not internal list."""
        task = Task(id=1, title="Test")
        repo.add(task)
        tasks1 = repo.find_all()
        tasks2 = repo.find_all()
        assert tasks1 == tasks2
        assert tasks1 is not tasks2  # Different list objects


class TestTaskServiceWithMocks:
    """Tests for TaskService with mocked storage."""

    @pytest.fixture
    def mock_storage(self) -> Mock:
        """Create a mock storage module."""
        with patch('app.load_tasks') as mock_load, \
             patch('app.save_tasks') as mock_save:
            yield {'load': mock_load, 'save': mock_save}

    def test_create_task_with_mocked_storage(self, mock_storage: dict) -> None:
        """Test creating a task with mocked storage."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        task = service.create_task("New Task")
        
        assert task.id == 1
        assert task.title == "New Task"
        assert task.done is False
        # Verify save was called
        mock_storage['save'].assert_called()

    def test_create_task_increments_id(self, mock_storage: dict) -> None:
        """Test that create_task increments IDs correctly."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_with_empty_title_raises_error(self, mock_storage: dict) -> None:
        """Test that empty title raises ValueError."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        with pytest.raises(ValueError):
            service.create_task("")

    def test_create_task_with_whitespace_only_raises_error(self, mock_storage: dict) -> None:
        """Test that whitespace-only title raises ValueError."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        with pytest.raises(ValueError):
            service.create_task("   ")

    def test_create_task_strips_whitespace(self, mock_storage: dict) -> None:
        """Test that title whitespace is stripped."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        task = service.create_task("  Test Task  ")
        assert task.title == "Test Task"

    def test_retrieve_all_tasks_empty(self, mock_storage: dict) -> None:
        """Test retrieving tasks from empty storage."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        tasks = service.retrieve_all_tasks()
        assert len(tasks) == 0

    def test_retrieve_all_tasks_with_mocked_data(self, mock_storage: dict) -> None:
        """Test retrieving multiple tasks from mocked storage."""
        mock_storage['load'].return_value = [
            {"id": 1, "title": "Task 1", "done": False},
            {"id": 2, "title": "Task 2", "done": True},
        ]
        service = TaskService("test.json")
        
        tasks = service.retrieve_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].done is True

    def test_retrieve_task_by_id_existing(self, mock_storage: dict) -> None:
        """Test retrieving a specific task by ID."""
        mock_storage['load'].return_value = [
            {"id": 1, "title": "Test Task", "done": False},
        ]
        service = TaskService("test.json")
        
        task = service.retrieve_task_by_id(1)
        assert task.title == "Test Task"

    def test_retrieve_task_by_id_missing_raises_error(self, mock_storage: dict) -> None:
        """Test that retrieving non-existent task raises TaskNotFoundError."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.retrieve_task_by_id(999)
        assert "999" in str(exc_info.value)

    def test_update_task_completion_toggles(self, mock_storage: dict) -> None:
        """Test toggling task completion status."""
        mock_storage['load'].return_value = [
            {"id": 1, "title": "Test", "done": False},
        ]
        service = TaskService("test.json")
        
        # First toggle: False -> True
        updated = service.update_task_completion(1)
        assert updated.done is True
        
        # Reset mock to return updated state
        mock_storage['load'].return_value = [
            {"id": 1, "title": "Test", "done": True},
        ]
        
        # Second toggle: True -> False
        updated = service.update_task_completion(1)
        assert updated.done is False

    def test_update_task_completion_missing_raises_error(self, mock_storage: dict) -> None:
        """Test that toggling non-existent task raises TaskNotFoundError."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.update_task_completion(999)
        assert "999" in str(exc_info.value)

    def test_delete_task_existing(self, mock_storage: dict) -> None:
        """Test deleting an existing task."""
        mock_storage['load'].return_value = [
            {"id": 1, "title": "Test", "done": False},
        ]
        service = TaskService("test.json")
        
        # Delete should not raise
        service.delete_task(1)
        mock_storage['save'].assert_called()

    def test_delete_task_missing_raises_error(self, mock_storage: dict) -> None:
        """Test that deleting non-existent task raises TaskNotFoundError."""
        mock_storage['load'].return_value = []
        service = TaskService("test.json")
        
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.delete_task(999)
        assert "999" in str(exc_info.value)


class TestTaskServiceIntegration:
    """Integration tests for TaskService with real file I/O."""

    @pytest.fixture
    def test_file(self) -> str:
        """Create a temporary test file path."""
        path = "test_tasks_integration.json"
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    def test_create_task_persists(self, test_file: str) -> None:
        """Test that created tasks are persisted to disk."""
        service = TaskService(test_file)
        task = service.create_task("Persistent Task")
        
        # Verify file was created
        assert os.path.exists(test_file)

    def test_persistence_across_instances(self, test_file: str) -> None:
        """Test that tasks persist across service instances."""
        # Create task with first instance
        service1 = TaskService(test_file)
        task = service1.create_task("Persistent Task")
        task_id = task.id
        
        # Create new service instance with same file
        service2 = TaskService(test_file)
        
        # Verify task was persisted
        retrieved = service2.retrieve_task_by_id(task_id)
        assert retrieved.title == "Persistent Task"
        assert retrieved.done is False

    def test_update_persists_across_instances(self, test_file: str) -> None:
        """Test that updates persist across service instances."""
        # Create and update task
        service1 = TaskService(test_file)
        task = service1.create_task("Test Task")
        service1.update_task_completion(task.id)
        
        # Create new instance and verify update persisted
        service2 = TaskService(test_file)
        retrieved = service2.retrieve_task_by_id(task.id)
        assert retrieved.done is True

    def test_delete_persists_across_instances(self, test_file: str) -> None:
        """Test that deletions persist across service instances."""
        # Create task
        service1 = TaskService(test_file)
        task = service1.create_task("Task to Delete")
        task_id = task.id
        
        # Delete task
        service1.delete_task(task_id)
        
        # Create new instance and verify task is gone
        service2 = TaskService(test_file)
        with pytest.raises(TaskNotFoundError):
            service2.retrieve_task_by_id(task_id)

    def test_multiple_tasks_persist(self, test_file: str) -> None:
        """Test that multiple tasks persist correctly."""
        service1 = TaskService(test_file)
        service1.create_task("Task 1")
        service1.create_task("Task 2")
        service1.create_task("Task 3")
        
        service2 = TaskService(test_file)
        tasks = service2.retrieve_all_tasks()
        assert len(tasks) == 3
        assert [t.title for t in tasks] == ["Task 1", "Task 2", "Task 3"]


class TestStorage:
    """Tests for Storage class."""

    @pytest.fixture
    def test_file(self) -> str:
        """Create a temporary test file path."""
        path = "test_storage_unit.json"
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    def test_load_from_nonexistent_file(self, test_file: str) -> None:
        """Test loading from non-existent file returns empty list."""
        storage = Storage(test_file)
        tasks = storage.load_tasks()
        assert tasks == []

    def test_save_and_load_tasks(self, test_file: str) -> None:
        """Test saving and loading tasks."""
        test_data = [
            {"id": 1, "title": "Task 1", "done": False},
            {"id": 2, "title": "Task 2", "done": True},
        ]
        storage = Storage(test_file)
        storage.save_tasks(test_data)
        
        loaded = storage.load_tasks()
        assert loaded == test_data

    def test_save_creates_file(self, test_file: str) -> None:
        """Test that save_tasks creates the file if missing."""
        assert not os.path.exists(test_file)
        storage = Storage(test_file)
        storage.save_tasks([])
        assert os.path.exists(test_file)

    def test_save_overwrites_existing(self, test_file: str) -> None:
        """Test that save_tasks overwrites existing file."""
        storage = Storage(test_file)
        storage.save_tasks([{"id": 1, "title": "Old", "done": False}])
        
        # Overwrite
        storage.save_tasks([{"id": 2, "title": "New", "done": True}])
        
        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0]["title"] == "New"

    def test_load_invalid_json_returns_empty(self, test_file: str) -> None:
        """Test that loading corrupted JSON file returns empty list."""
        # Write invalid JSON
        with open(test_file, 'w') as f:
            f.write("{ invalid json }")
        
        storage = Storage(test_file)
        tasks = storage.load_tasks()
        assert tasks == []

    def test_add_task(self, test_file: str) -> None:
        """Test adding a task to storage."""
        storage = Storage(test_file)
        task = {"id": 1, "title": "New Task", "done": False}
        storage.add_task(task)
        
        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0]["title"] == "New Task"

    def test_delete_task_existing(self, test_file: str) -> None:
        """Test deleting an existing task."""
        storage = Storage(test_file)
        storage.save_tasks([
            {"id": 1, "title": "Task 1", "done": False},
            {"id": 2, "title": "Task 2", "done": False},
        ])
        
        result = storage.delete_task(1)
        assert result is True
        
        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0]["id"] == 2

    def test_delete_task_nonexistent(self, test_file: str) -> None:
        """Test deleting a non-existent task."""
        storage = Storage(test_file)
        storage.save_tasks([{"id": 1, "title": "Task", "done": False}])
        
        result = storage.delete_task(999)
        assert result is False

    def test_update_task_existing(self, test_file: str) -> None:
        """Test updating an existing task."""
        storage = Storage(test_file)
        storage.save_tasks([{"id": 1, "title": "Original", "done": False}])
        
        result = storage.update_task(1, {"title": "Updated", "done": True})
        assert result is True
        
        loaded = storage.load_tasks()
        assert loaded[0]["title"] == "Updated"
        assert loaded[0]["done"] is True

    def test_update_task_nonexistent(self, test_file: str) -> None:
        """Test updating a non-existent task."""
        storage = Storage(test_file)
        storage.save_tasks([{"id": 1, "title": "Task", "done": False}])
        
        result = storage.update_task(999, {"done": True})
        assert result is False


class TestCompleteWorkflow:
    """Integration tests for complete task workflow: create -> toggle -> delete."""

    @pytest.fixture
    def test_file(self) -> str:
        """Create a temporary test file path."""
        path = "test_workflow.json"
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    def test_complete_workflow_create_toggle_delete(self, test_file: str) -> None:
        """Test complete workflow: add task -> toggle completion -> delete."""
        service = TaskService(test_file)
        
        # Step 1: Create a new task
        task = service.create_task("Complete Workflow Test")
        task_id = task.id
        assert task.title == "Complete Workflow Test"
        assert task.done is False
        
        # Verify file was created with the task
        assert os.path.exists(test_file)
        
        # Verify task is persisted
        retrieved = service.retrieve_task_by_id(task_id)
        assert retrieved.title == "Complete Workflow Test"
        assert retrieved.done is False
        
        # Step 2: Toggle completion (mark as done)
        updated = service.update_task_completion(task_id)
        assert updated.done is True
        
        # Verify toggle persisted
        retrieved = service.retrieve_task_by_id(task_id)
        assert retrieved.done is True
        
        # Step 3: Toggle again (mark as not done)
        updated = service.update_task_completion(task_id)
        assert updated.done is False
        
        # Verify second toggle persisted
        retrieved = service.retrieve_task_by_id(task_id)
        assert retrieved.done is False
        
        # Step 4: Delete the task
        service.delete_task(task_id)
        
        # Verify task is deleted
        with pytest.raises(TaskNotFoundError):
            service.retrieve_task_by_id(task_id)
        
        # Verify no tasks remain
        all_tasks = service.retrieve_all_tasks()
        assert len(all_tasks) == 0

    def test_workflow_with_multiple_tasks(self, test_file: str) -> None:
        """Test workflow with multiple tasks in different states."""
        service = TaskService(test_file)
        
        # Create multiple tasks
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")
        
        # Initial state: all incomplete
        assert service.retrieve_all_tasks() == [task1, task2, task3]
        
        # Toggle first task to done
        service.update_task_completion(task1.id)
        
        # Verify state
        all_tasks = service.retrieve_all_tasks()
        assert all_tasks[0].done is True
        assert all_tasks[1].done is False
        assert all_tasks[2].done is False
        
        # Toggle second task to done
        service.update_task_completion(task2.id)
        
        # Delete first task
        service.delete_task(task1.id)
        
        # Verify final state: 2 tasks remain, second is done, third is incomplete
        all_tasks = service.retrieve_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].title == "Task 2"
        assert all_tasks[0].done is True
        assert all_tasks[1].title == "Task 3"
        assert all_tasks[1].done is False

    def test_workflow_persists_across_instances(self, test_file: str) -> None:
        """Test that complete workflow state persists across service instances."""
        # First instance: create and toggle
        service1 = TaskService(test_file)
        task = service1.create_task("Persistence Test")
        service1.update_task_completion(task.id)
        
        # Second instance: verify state and delete
        service2 = TaskService(test_file)
        retrieved = service2.retrieve_task_by_id(task.id)
        assert retrieved.title == "Persistence Test"
        assert retrieved.done is True
        
        # Delete via second instance
        service2.delete_task(task.id)
        
        # Third instance: verify deletion persisted
        service3 = TaskService(test_file)
        with pytest.raises(TaskNotFoundError):
            service3.retrieve_task_by_id(task.id)

    def test_workflow_with_error_handling(self, test_file: str) -> None:
        """Test workflow includes proper error handling."""
        service = TaskService(test_file)
        
        # Test that invalid operations raise appropriate errors
        with pytest.raises(TaskNotFoundError):
            service.update_task_completion(999)
        
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)
        
        with pytest.raises(TaskNotFoundError):
            service.retrieve_task_by_id(999)
        
        # Valid task should still work after errors
        task = service.create_task("After Error")
        retrieved = service.retrieve_task_by_id(task.id)
        assert retrieved.title == "After Error"
        
        # Can delete valid task
        service.delete_task(task.id)
        
        # Further operations on deleted task should fail
        with pytest.raises(TaskNotFoundError):
            service.retrieve_task_by_id(task.id)


# Test execution helpers
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
