# Copilot Prompt Templates for Task Manager

This document provides ready-to-use prompt templates for common development tasks with the Task Manager project.

## Quick Template

Copy and customize this template:

```markdown
# Intention:
[What you want to build/fix/improve]

# Constraints:
[Technical limits: Python version, style, dependencies, max size]

# Example:
[Show input → expected output or current → desired behavior]
```

---

## Feature Request Templates

### Template: New Command

```markdown
# Intention:
Add a new `<command_name>` command to list tasks filtered by completion status

# Constraints:
- Use argparse subparser like existing commands (add, list, toggle, delete)
- Output format should match existing list command
- Keep implementation under 20 lines (excluding docstring)
- No external dependencies

# Example:
Command: py cli.py list --status done
Output:
[2] Write documentation - DONE

# Questions for Copilot:
1. Where in cli.py should this go?
2. Should I modify the existing list_parser or create a new one?
```

### Template: Data Enhancement

```markdown
# Intention:
Add a `created_at` timestamp to tasks when they are created

# Constraints:
- Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Update Task dataclass in app.py
- Update storage.py to handle migration of old tasks (no timestamp)
- Update tests in test_app.py

# Current Behavior:
Tasks only store: id, title, done

# Desired Behavior:
Tasks also store: id, title, done, created_at
Example: {"id": 1, "title": "Test", "done": false, "created_at": "2025-12-01T14:30:45"}

# Output Format in List:
[1] Test - NOT DONE (created: Dec 01, 2025)
```

### Template: UI Improvement

```markdown
# Intention:
Color-code task output: incomplete tasks in yellow, complete in green

# Constraints:
- Use ANSI color codes (no external colorama library)
- Only apply colors to status part, not the entire line
- Must work on Windows, macOS, and Linux terminals

# Current Output:
[1] Buy groceries - NOT DONE
[2] Write docs - DONE

# Desired Output:
[1] Buy groceries - \033[93mNOT DONE\033[0m  (yellow)
[2] Write docs - \033[92mDONE\033[0m        (green)

# Questions:
1. Should color codes be hardcoded or use a function?
2. How do I handle Windows Terminal compatibility?
```

---

## Bug Fix Templates

### Template: Missing Feature

```markdown
# Intention:
Tasks should be sortable by creation date (newest first by default)

# Constraints:
- Use existing JSON storage format
- Don't break backward compatibility
- Add optional --sort parameter to list command
- Test with 5+ tasks

# Current Behavior:
py cli.py list
[3] Task 3 - NOT DONE
[2] Task 2 - NOT DONE
[1] Task 1 - NOT DONE
(appears in ID order, not creation order)

# Desired Behavior:
py cli.py list --sort date
[3] Task 3 - NOT DONE (2025-12-01)
[2] Task 2 - NOT DONE (2025-11-30)
[1] Task 1 - NOT DONE (2025-11-29)
(sorted by most recently created first)

# Files to Modify:
- cli.py (add --sort parameter)
- app.py (add sort logic to TaskService)
```

### Template: Unexpected Behavior

```markdown
# Intention:
Fix: When I add a task and immediately check the file, sometimes tasks.json is empty

# Constraints:
- Must not add external dependencies
- Keep changes minimal (focused on the bug)
- Ensure thread-safe writes if possible

# Reproduction Steps:
1. py cli.py add "Test 1"
2. (pause 1 second)
3. py cli.py list
Expected: Task appears
Actual: No tasks shown (sometimes)

# Root Cause Analysis:
File might not be flushed before process exits. Check _persist() method.

# Questions:
1. Should I add explicit flush()?
2. Do I need to catch file I/O exceptions?
```

---

## Testing Templates

### Template: Unit Test

```markdown
# Intention:
Write unit tests for TaskService.add_task() method

# Constraints:
- Use unittest framework (already imported in test_app.py)
- Each test should be independent
- Test both happy path and error cases
- Tests should pass with existing storage.py

# Test Cases:
1. add_task returns a Task object with correct id
2. add_task with empty string title (should it fail or succeed?)
3. add_task persists to disk (verify tasks.json updated)
4. Multiple add_task calls increment id correctly

# Example Test Structure:
class TestAddTask(unittest.TestCase):
    def setUp(self):
        # Create fresh service for each test
    
    def test_add_task_returns_task_object(self):
        # Assert result is a Task
    
    def tearDown(self):
        # Cleanup tasks.json if needed
```

### Template: Integration Test

```markdown
# Intention:
Write an integration test that simulates a complete workflow: add → list → toggle → delete

# Constraints:
- Use real TaskService (not mocks) with real JSON storage
- Clean up test data after running
- Test should run in < 1 second
- Use temporary test file, not actual tasks.json

# Workflow to Test:
1. Create service
2. Add 3 tasks
3. Toggle task 2
4. Delete task 1
5. Verify final state (tasks 2 and 3 remain, task 2 is done)

# Example:
def test_complete_workflow(self):
    svc = TaskService(filename="test_tasks_temp.json")
    # ... steps ...
    finally:
        os.remove("test_tasks_temp.json")  # cleanup
```

---

## Documentation Templates

### Template: Function Docstring

```markdown
# Intention:
Write a comprehensive docstring for the format_task() function in cli.py

# Constraints:
- Use Google-style docstring format
- Include Parameters, Returns, and Examples sections
- Keep example simple and runnable
- Show both possible status values

# Current Function:
def format_task(task_id: int, title: str, done: bool) -> str:
    status = "DONE" if done else "NOT DONE"
    return f"[{task_id}] {title} - {status}"

# Desired Docstring Format:
\"\"\"
    Brief description.
    
    Parameters:
        task_id: ...
        title: ...
        done: ...
    
    Returns:
        ...
    
    Examples:
        >>> format_task(1, "Buy milk", False)
        '[1] Buy milk - NOT DONE'
\"\"\"
```

### Template: README Section

```markdown
# Intention:
Add a "Performance" section to README.md

# Constraints:
- Keep under 150 words
- Include real performance metrics if running tests
- Make actionable recommendations
- Focus on user-facing performance, not code internals

# Topics to Cover:
- Typical command latency (add/list/toggle/delete)
- File size limits (how many tasks before slowdown?)
- Recommendations (when to archive old tasks)
- Future optimizations

# Format:
Use markdown with code blocks for commands and output
```

---

## Refactoring Templates

### Template: Code Cleanup

```markdown
# Intention:
Reduce code duplication in cli.py by extracting common error handling

# Constraints:
- Must maintain same functionality (no behavior changes)
- Keep same error messages for user-facing output
- Don't introduce new functions that aren't used

# Current Code Pattern:
Appears 3 times in cmd_toggle, cmd_delete, etc.:
if service.<operation>(args.id):
    print("✓ ...")
else:
    print(f"✗ Task {args.id} not found.")

# Desired Refactoring:
Create helper function: handle_task_operation(operation, task_id, success_msg)
Then use it in all commands
```

### Template: Performance Optimization

```markdown
# Intention:
Optimize TaskService to cache tasks in memory and reduce disk reads by 80%

# Constraints:
- Must maintain backward compatibility (same public API)
- Add a refresh() method to force reload when needed
- Handle concurrent access from other processes (still read from disk on list)
- No external dependencies

# Current Behavior:
Every list_tasks() call reloads entire file from disk

# Desired Behavior:
Cache tasks in memory for 5 seconds, then re-read
Add explicit refresh() method for immediate reload

# Metrics:
Before: 100 list_tasks() calls = 100 disk reads
After: 100 list_tasks() calls (within 5 sec) = 1 disk read
```

---

## Enhancement Templates

### Template: New Feature

```markdown
# Intention:
Add support for task descriptions (longer text than just title)

# Constraints:
- Don't break existing tasks without descriptions
- Keep JSON storage format simple
- Add optional --description flag to add command
- Display in list command (indented, on separate line)

# Example Usage:
py cli.py add "Learn Python" --description "Focus on OOP concepts"

# New JSON Format:
{
  "id": 1,
  "title": "Learn Python",
  "done": false,
  "description": "Focus on OOP concepts"
}

# Display Format in List:
[1] Learn Python - NOT DONE
    Description: Focus on OOP concepts

# Files to Modify:
- Task dataclass (add description field)
- cli.py (add --description arg)
- storage functions (handle optional description)
```

### Template: Import New Library

```markdown
# Intention:
Add colored output using the 'colorama' library

# Constraints:
- Update requirements.txt with version
- Create utility function color_status(status_string)
- Only color the status part, not IDs or titles
- Test on Windows and Unix terminals

# Library Details:
- Name: colorama
- Version: 0.4.6+
- Usage: from colorama import Fore

# Example:
from colorama import Fore, Style
colored = f"{Fore.GREEN}DONE{Style.RESET_ALL}"
```

---

## Test This Prompt Template

To verify a prompt works well, ask Copilot:

```markdown
# Intention:
[Your prompt here]

# Test Checklist:
- [] Is the generated code syntactically correct?
- [] Does it follow the project's style (PEP8, type hints)?
- [] Does it satisfy all constraints?
- [] Can you run it without errors?
- [] Does it solve the stated problem?

# If any [] is unchecked, provide feedback:
"The code works but doesn't include error handling for X"
```

---

## Resources

- **Python Docs:** https://docs.python.org/3/
- **PEP 8 Style Guide:** https://www.python.org/dev/peps/pep-0008/
- **Google Docstring Format:** https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
- **argparse Tutorial:** https://docs.python.org/3/library/argparse.html
