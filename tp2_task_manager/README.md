# Task Manager Application

A simple command-line task manager application written in Python with persistent JSON storage.

## Features

- ✅ **Add Tasks** - Create new tasks with titles
- ✅ **List Tasks** - View all tasks with their status (DONE or NOT DONE)
- ✅ **Toggle Tasks** - Mark tasks as done/not done
- ✅ **Delete Tasks** - Remove tasks from the list
- ✅ **Persistent Storage** - Tasks are saved to a JSON file (`tasks.json`)
- ✅ **Clean CLI Interface** - Uses argparse for professional command-line experience

## Project Structure

```
tp2_task_manager/
├── app.py          # Task dataclass and TaskService (business logic)
├── cli.py          # Command-line interface with argparse
├── storage.py      # JSON file storage backend
├── config.py       # Configuration constants
├── test_app.py     # Unit tests
├── setup.py        # Package setup configuration
├── setup_env.py    # Environment setup script
├── requirements.txt # Project dependencies
├── README.md       # This file
└── tasks.json      # Task storage file (auto-created on first run)
```

## Installation & Setup

### 1. Ensure Python is installed
Download and install Python 3.7+ from [python.org](https://www.python.org/downloads/):
- During installation, **check** "Add Python to PATH"

### 2. Create and activate a virtual environment (recommended)

**Windows (PowerShell):**
```powershell
cd c:\Formation\githubcopilot\tp2_task_manager
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
cd ~/Formation/githubcopilot/tp2_task_manager
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies (optional, none required for basic use)
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

```bash
# Add a task
py cli.py add "Apprendre Copilot"
py cli.py add "Buy groceries"
py cli.py add "Write documentation"

# List all tasks
py cli.py list

# Toggle task completion (mark as done/not done)
py cli.py toggle 1
py cli.py toggle 2

# Delete a task
py cli.py delete 2

# View help
py cli.py --help
py cli.py add --help
```

### Output Format

When you list tasks, the output looks like:
```
============================================================
                        TASKS
============================================================
[1] Apprendre Copilot - NOT DONE
[2] Buy groceries - DONE
[3] Write documentation - NOT DONE
============================================================
```

Each task is displayed as: `[id] title - status`
- `NOT DONE`: Task is pending
- `DONE`: Task is completed

### Example Workflow

```powershell
# Add tasks
PS> py cli.py add "Learn Python"
✓ Task added: [1] Learn Python - NOT DONE

PS> py cli.py add "Build a project"
✓ Task added: [2] Build a project - NOT DONE

# List tasks
PS> py cli.py list
============================================================
                        TASKS
============================================================
[1] Learn Python - NOT DONE
[2] Build a project - NOT DONE
============================================================

# Complete first task
PS> py cli.py toggle 1
✓ Task 1 toggled: [1] Learn Python - DONE

# List again to verify
PS> py cli.py list
============================================================
                        TASKS
============================================================
[1] Learn Python - DONE
[2] Build a project - NOT DONE
============================================================

# Delete the completed task
PS> py cli.py delete 1
✓ Task 1 deleted.

# List final state
PS> py cli.py list
============================================================
                        TASKS
============================================================
[2] Build a project - NOT DONE
============================================================
```

## Data Storage

Tasks are stored in `tasks.json` in the following format:

```json
[
  {
    "id": 1,
    "title": "Learn Python",
    "done": true
  },
  {
    "id": 2,
    "title": "Build a project",
    "done": false
  }
]
```

The file is automatically:
- Created on first task addition
- Updated after every operation (add, toggle, delete)
- Loaded on each CLI invocation to ensure consistency

## Architecture

### Task (dataclass)
Represents a single task with:
- `id: int` - Unique identifier
- `title: str` - Task description
- `done: bool` - Completion flag (default: False)

### TaskService
In-memory service that:
- Loads tasks from `tasks.json` on initialization
- Provides CRUD operations: `add_task()`, `list_tasks()`, `toggle_task()`, `delete_task()`
- Persists changes to disk automatically
- Automatically manages task IDs

### CLI Interface
Command-line interface using `argparse`:
- Subcommands: `add`, `list`, `toggle`, `delete`
- Clean help messages and examples
- Input validation and error handling

### Storage
Handles JSON file I/O:
- `load_tasks()` - Load from disk (returns empty list if file missing)
- `save_tasks()` - Save to disk with proper formatting
- Handles file creation automatically

## Running Tests

Run unit tests for TaskService and Storage:

```bash
python test_app.py
```

Tests cover:
- Loading tasks from empty/missing file
- Adding tasks
- Updating task state
- Deleting tasks
- ID management

## PEP8 Compliance

This project follows PEP8 style guidelines:
- ✅ Clear, descriptive naming conventions
- ✅ Comprehensive docstrings (Google style)
- ✅ Type hints on all functions
- ✅ Proper spacing and formatting
- ✅ Modular, single-responsibility design

## Architecture Decisions

1. **Task as dataclass** - Clean, simple representation with automatic `__init__`, `__repr__`, etc.
2. **TaskService for business logic** - Separates data handling from CLI/storage concerns
3. **Automatic persistence** - Tasks are saved to disk after every operation
4. **argparse for CLI** - Standard Python tool with excellent help/validation support
5. **Simple JSON storage** - No external database dependency, human-readable file format

## Future Enhancements

- [ ] Due dates and deadline tracking
- [ ] Task priorities (high/medium/low)
- [ ] Categories or tags
- [ ] Search and filter functionality
- [ ] Recurring tasks
- [ ] Export to CSV/PDF
- [ ] Web-based interface (Flask/FastAPI)
- [ ] User authentication and multi-user support
- [ ] Sync across devices
- [ ] Task descriptions (not just titles)

## Troubleshooting

### "Python is not found" or "py is not recognized"
- Ensure Python 3.7+ is installed from [python.org](https://www.python.org/downloads/)
- During installation, **check the box** "Add Python to PATH"
- Restart PowerShell/Terminal after installation
- Try `python --version` or `py --version` to verify

### Tasks not persisting
- Check that `tasks.json` is created in the same directory as `cli.py`
- Ensure you have write permissions in the directory
- Tasks are saved after each operation automatically

### Import errors when running cli.py
- Ensure you're in the correct directory: `cd c:\Formation\githubcopilot\tp2_task_manager`
- Ensure `app.py` and `storage.py` are in the same directory
- If using a virtual environment, make sure it's activated

## License

This project is provided as-is for educational purposes.

## Author

Created as a learning project for Python development with argparse, dataclasses, and JSON storage.
