# Task Manager CLI - Usage Guide

Complete guide for using the Task Manager command-line application with installation, commands, examples, and best practices for Copilot prompts.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Commands Reference](#commands-reference)
4. [Reproducible Examples](#reproducible-examples)
5. [Copilot Prompt Best Practices](#copilot-prompt-best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- **Python 3.7 or higher** installed on your system
- Access to command-line/terminal/PowerShell

### Step 1: Download Python

Visit [python.org](https://www.python.org/downloads/) and download the latest Python installer.

**Windows Installation Notes:**
- During installation, **CHECK** "Add Python to PATH" (important!)
- Choose "Install for all users" or "Current user"
- Complete the installation

**macOS Installation Notes:**
- Python 3 comes pre-installed, but you can upgrade via [python.org](https://www.python.org/downloads/)
- Or use Homebrew: `brew install python3`

**Linux Installation Notes:**
- Ubuntu/Debian: `sudo apt-get install python3 python3-pip`
- Fedora: `sudo dnf install python3 python3-pip`
- Arch: `sudo pacman -S python`

### Step 2: Verify Python Installation

Open your terminal/PowerShell and run:

```bash
python --version
# or
python3 --version
# or (Windows with Python Launcher)
py --version
```

You should see output like: `Python 3.11.6`

### Step 3: Navigate to Project Directory

```bash
# Windows (PowerShell)
cd c:\Formation\githubcopilot\tp2_task_manager

# macOS/Linux
cd ~/Formation/githubcopilot/tp2_task_manager
```

### Step 4: Create Virtual Environment (Recommended)

A virtual environment isolates project dependencies.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux (Bash/Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You'll see `(.venv)` appear in your prompt when activated.

### Step 5: Install Dependencies (Optional)

The project has minimal dependencies. Optional packages for development:

```bash
pip install -r requirements.txt
```

This installs testing and code-quality tools (pytest, black, flake8, mypy).

---

## Quick Start

Once installed, here are the most common commands:

```bash
# Add a new task
py cli.py add "Learn Python basics"

# List all tasks
py cli.py list

# Mark task 1 as done
py cli.py toggle 1

# Delete task 2
py cli.py delete 2

# Get help
py cli.py --help
```

---

## Commands Reference

### 1. Add a Task

**Syntax:**
```bash
py cli.py add "<task_title>"
```

**Parameters:**
- `<task_title>`: String describing the task (use quotes if spaces)

**Examples:**
```bash
py cli.py add "Buy groceries"
py cli.py add "Write Python unit tests"
py cli.py add "Review code changes"
```

**Output:**
```
✓ Task added: [1] Buy groceries - NOT DONE
```

**Notes:**
- Task IDs are auto-generated (starting from 1)
- Tasks are saved immediately to `tasks.json`
- Title is required; cannot be empty

---

### 2. List Tasks

**Syntax:**
```bash
py cli.py list
```

**Parameters:**
None

**Example:**
```bash
py cli.py list
```

**Output:**
```
============================================================
                        TASKS
============================================================
[1] Buy groceries - NOT DONE
[2] Write Python unit tests - DONE
[3] Review code changes - NOT DONE
============================================================
```

**Notes:**
- Shows all tasks with their IDs and completion status
- Reloads from disk each time (reflects changes by other processes)
- Empty list message if no tasks exist

---

### 3. Toggle Task Completion

**Syntax:**
```bash
py cli.py toggle <task_id>
```

**Parameters:**
- `<task_id>`: Integer ID of the task (required, no quotes)

**Examples:**
```bash
py cli.py toggle 1
py cli.py toggle 3
```

**Output:**
```
✓ Task 1 toggled: [1] Buy groceries - DONE
```

**Notes:**
- Switches task between NOT DONE and DONE
- Returns error if task ID doesn't exist
- Change is persisted immediately

---

### 4. Delete a Task

**Syntax:**
```bash
py cli.py delete <task_id>
```

**Parameters:**
- `<task_id>`: Integer ID of the task (required, no quotes)

**Examples:**
```bash
py cli.py delete 2
py cli.py delete 1
```

**Output:**
```
✓ Task 1 deleted.
```

**Notes:**
- Removes task completely (cannot be undone)
- Subsequent task IDs remain unchanged
- Returns error if task ID doesn't exist

---

### 5. Help

**Syntax:**
```bash
py cli.py --help
py cli.py add --help
py cli.py list --help
py cli.py toggle --help
py cli.py delete --help
```

**Output:**
Shows command description, available arguments, and examples.

---

## Reproducible Examples

### Scenario 1: Daily Task Workflow

**Goal:** Set up and track daily work tasks.

**Step 1: Add morning tasks**
```bash
py cli.py add "Check emails"
py cli.py add "Team standup meeting"
py cli.py add "Code review"
```

**Expected output:**
```
✓ Task added: [1] Check emails - NOT DONE
✓ Task added: [2] Team standup meeting - NOT DONE
✓ Task added: [3] Code review - NOT DONE
```

**Step 2: View all tasks**
```bash
py cli.py list
```

**Expected output:**
```
============================================================
                        TASKS
============================================================
[1] Check emails - NOT DONE
[2] Team standup meeting - NOT DONE
[3] Code review - NOT DONE
============================================================
```

**Step 3: Complete tasks as you finish them**
```bash
py cli.py toggle 1
py cli.py toggle 2
```

**Step 4: View progress**
```bash
py cli.py list
```

**Expected output:**
```
============================================================
                        TASKS
============================================================
[1] Check emails - DONE
[2] Team standup meeting - DONE
[3] Code review - NOT DONE
============================================================
```

**Step 5: Clean up completed tasks**
```bash
py cli.py delete 1
py cli.py delete 2
```

---

### Scenario 2: Project Planning

**Goal:** Manage a software project with multiple features.

**Add project tasks:**
```bash
py cli.py add "Design database schema"
py cli.py add "Implement user authentication"
py cli.py add "Create API endpoints"
py cli.py add "Write unit tests"
py cli.py add "Deploy to production"
```

**Check progress:**
```bash
py cli.py list
```

**Complete initial work:**
```bash
py cli.py toggle 1
py cli.py toggle 2
```

**Add urgent task in between:**
```bash
py cli.py add "Fix critical bug"
```

**View updated list:**
```bash
py cli.py list
```

---

### Scenario 3: Learning Plan

**Goal:** Track Python learning milestones.

**Create learning checklist:**
```bash
py cli.py add "Learn Python basics (variables, loops, functions)"
py cli.py add "Understand OOP (classes, inheritance, polymorphism)"
py cli.py add "Master async/await for concurrent programming"
py cli.py add "Build a REST API with Flask"
py cli.py add "Write comprehensive unit tests"
```

**Mark completed lessons:**
```bash
py cli.py toggle 1
py cli.py toggle 2
```

**View learning progress:**
```bash
py cli.py list
```

**Add new topic discovered:**
```bash
py cli.py add "Explore decorators and metaclasses"
```

---

## Copilot Prompt Best Practices

When using GitHub Copilot to write prompts for this Task Manager, follow this framework:

### Structure of an Effective Copilot Prompt

A good prompt contains three parts:

1. **Intention** - What do you want to accomplish? (Clear goal)
2. **Constraints** - What are the limits? (Size, style, format, language)
3. **Example** - What does success look like? (Input → Expected output)

---

### Example 1: Adding a Feature

**❌ Bad Prompt:**
```
Add a feature to filter tasks
```

**Why it's unclear:**
- Unclear filter type (by status? by date?)
- No example of expected behavior
- Doesn't specify constraints

**✅ Good Prompt:**
```
# Intention:
Add a command to filter and display only incomplete tasks in the CLI

# Constraints:
- Use argparse like existing commands
- Format output same as list command
- Keep it under 15 lines of code

# Example:
py cli.py list --filter incomplete
Output:
============================================================
                        TASKS (INCOMPLETE)
============================================================
[1] Buy groceries - NOT DONE
[3] Review code changes - NOT DONE
============================================================
```

---

### Example 2: Bug Fix

**❌ Bad Prompt:**
```
Fix the bug where tasks aren't saved
```

**Why it's unclear:**
- Doesn't describe the bug behavior
- Doesn't specify reproduction steps
- No expected vs actual output

**✅ Good Prompt:**
```
# Intention:
Fix bug where newly added tasks disappear after closing and reopening the app

# Constraints:
- Must work with existing JSON storage (storage.py)
- Should handle file permission errors gracefully
- No external dependencies

# Reproduction Steps:
1. Run: py cli.py add "Test task"
2. Run: py cli.py list (task shows)
3. Close terminal and reopen
4. Run: py cli.py list (task SHOULD show but doesn't)

# Expected Behavior:
Tasks persist in tasks.json and reappear on next run
```

---

### Example 3: Code Refactoring

**❌ Bad Prompt:**
```
Make TaskService more efficient
```

**Why it's vague:**
- Which aspect? (Memory? Speed? Readability?)
- No performance metrics
- Doesn't specify constraints

**✅ Good Prompt:**
```
# Intention:
Refactor TaskService to reduce file I/O by implementing lazy loading

# Constraints:
- Must maintain same public API (don't break existing calls)
- Keep all functionality (add, list, toggle, delete)
- Add caching only for list_tasks() to reduce disk reads

# Current Behavior:
list_tasks() reloads from disk every time (inefficient for repeated calls)

# Desired Behavior:
Cache tasks in memory, only reload when explicitly needed
Add a refresh() method to force reload from disk
```

---

### Example 4: Testing

**❌ Bad Prompt:**
```
Write tests for the app
```

**Why it's incomplete:**
- Which class/function?
- What test style? (unit, integration?)
- How many test cases?

**✅ Good Prompt:**
```
# Intention:
Write unit tests for TaskService toggle_task() method

# Constraints:
- Use Python unittest framework (already in imports)
- Test both success and failure cases
- Each test should be independent (no shared state)

# Test Cases to Cover:
1. Toggle existing task from NOT DONE → DONE
2. Toggle existing task from DONE → NOT DONE
3. Try to toggle non-existent task (return False)
4. Verify state persists to disk after toggle

# Example Test:
def test_toggle_task_changes_state(self):
    svc = TaskService()
    svc.add_task("Test")
    original_state = svc.list_tasks()[0].done
    svc.toggle_task(1)
    new_state = svc.list_tasks()[0].done
    self.assertNotEqual(original_state, new_state)
```

---

### Example 5: Documentation

**❌ Bad Prompt:**
```
Document the TaskService class
```

**Why it's vague:**
- Which documentation format?
- How detailed?
- Examples included?

**✅ Good Prompt:**
```
# Intention:
Create a detailed docstring for TaskService class following Google style

# Constraints:
- Include class-level description
- Document __init__ with parameter descriptions
- Add usage example showing typical workflow
- Limit to 30 lines including examples

# Content to Cover:
1. What the class does (manages persistent tasks)
2. How it works (loads from JSON, auto-saves)
3. Simple example: add → list → toggle → delete workflow

# Example Format:
\"\"\"
Task management service with JSON persistence.
    
Handles adding, listing, toggling, and deleting tasks with
automatic saving to tasks.json.
    
Examples:
    >>> svc = TaskService()
    >>> svc.add_task('Learn Python')
    Task(id=1, title='Learn Python', done=False)
\"\"\"
```

---

### Template for Your Own Prompts

Copy this template for consistency:

```markdown
# Intention:
[What do you want to accomplish? Be specific and measurable]

# Constraints:
[What are the limits? (lines of code, style, dependencies, format)]

# Example:
[Show input and expected output, or step-by-step scenario]

# Additional Context:
[Optional: current behavior, known issues, dependencies]
```

---

### Copilot Prompt Anti-Patterns (Avoid These)

| ❌ Anti-Pattern | ✅ Better Approach |
|---|---|
| "Make it better" | "Reduce function complexity by extracting a helper method" |
| "Fix the bug" | "Fix: tasks disappear after app restart. Root cause: file not flushed" |
| "Add comments" | "Add docstrings in Google style for get_next_id() method" |
| "Optimize" | "Reduce load_tasks() calls from 3 to 1 by caching in memory" |
| "Make it look nice" | "Use ANSI color codes to highlight DONE tasks in green" |

---

### Tips for Best Results with Copilot

1. **Be Specific:** Instead of "improve", say "reduce cyclomatic complexity to <10"
2. **Show Examples:** Paste the function you want to modify, plus expected output
3. **Define Constraints:** Specify language version, style guide, max lines
4. **Test the Code:** After Copilot generates code, run it: `py cli.py --help`
5. **Iterate:** If the result isn't perfect, provide feedback: "This adds too many parameters. Combine them into a Config object"

---

## Troubleshooting

### "Python is not found"

**Windows:**
```powershell
# Check if Python is installed
python --version
py --version

# If neither works, reinstall Python from python.org
# IMPORTANT: Check "Add Python to PATH" during installation
```

**macOS/Linux:**
```bash
python3 --version
# If not installed: brew install python3
```

### "tasks.json not found"

This is normal on first run. It will be created automatically when you add the first task:

```bash
py cli.py add "First task"
# Now tasks.json is created
py cli.py list
```

### "ModuleNotFoundError: No module named 'app'"

**Cause:** You're not in the correct directory.

**Solution:**
```bash
cd c:\Formation\githubcopilot\tp2_task_manager
py cli.py list
```

### "Task ID not found"

```bash
# Make sure the ID exists
py cli.py list  # View all IDs first

# Then use a valid ID
py cli.py toggle 1  # Use an ID from the list
```

### Virtual Environment Issues

```bash
# If (.venv) doesn't appear, activate it again
# Windows:
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# To deactivate (leave venv):
deactivate
```

### "Permission denied" when saving tasks

**Cause:** You don't have write permission in the directory.

**Solution:**
- Use a directory you own
- Or change directory permissions: `chmod 755 /path/to/tp2_task_manager`

---

## Next Steps

1. **Try the examples** in the "Reproducible Examples" section
2. **Experiment with prompts** using the framework in "Copilot Prompt Best Practices"
3. **Extend the app** by asking Copilot well-formed prompts
4. **Share your prompts** with the team if you find especially effective ones

Happy task managing! 🚀
