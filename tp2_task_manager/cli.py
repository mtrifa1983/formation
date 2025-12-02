"""
CLI Module - Command-line interface for Task Manager using argparse.

Provides a clean, argument-based interface for managing tasks with error handling.
"""

import argparse
import sys
from typing import Optional

from app import TaskService, TaskNotFoundError


def format_task(task_id: int, title: str, done: bool) -> str:
    """Format a task for display.
    
    Parameters
    ----------
    task_id : int
        The task ID.
    title : str
        The task title.
    done : bool
        Whether the task is completed.
    
    Returns
    -------
    str
        Formatted task string.
        
    Examples
    --------
    >>> format_task(1, "Buy milk", False)
    '[1] Buy milk - NOT DONE'
    >>> format_task(2, "Write docs", True)
    '[2] Write docs - DONE'
    """
    status = "DONE" if done else "NOT DONE"
    return f"[{task_id}] {title} - {status}"


def cmd_add(args: argparse.Namespace, service: TaskService) -> None:
    """Handle 'add' command to create a new task.
    
    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments containing 'title'.
    service : TaskService
        The task service instance.
    """
    try:
        task = service.create_task(args.title)
        print(f"✓ Task added: {format_task(task.id, task.title, task.done)}")
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args: argparse.Namespace, service: TaskService) -> None:
    """Handle 'list' command to display all tasks.
    
    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments (unused).
    service : TaskService
        The task service instance.
    """
    try:
        tasks = service.retrieve_all_tasks()
        if not tasks:
            print("No tasks found.")
            return
        
        print("\n" + "=" * 60)
        print("TASKS".center(60))
        print("=" * 60)
        for task in tasks:
            print(format_task(task.id, task.title, task.done))
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"✗ Error listing tasks: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_toggle(args: argparse.Namespace, service: TaskService) -> None:
    """Handle 'toggle' command to change task completion status.
    
    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments containing 'id'.
    service : TaskService
        The task service instance.
    """
    try:
        task = service.update_task_completion(args.id)
        print(f"✓ Task {args.id} toggled: {format_task(task.id, task.title, task.done)}")
    except TaskNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error toggling task: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_delete(args: argparse.Namespace, service: TaskService) -> None:
    """Handle 'delete' command to remove a task.
    
    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments containing 'id'.
    service : TaskService
        The task service instance.
    """
    try:
        service.delete_task(args.id)
        print(f"✓ Task {args.id} deleted.")
    except TaskNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error deleting task: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point with argparse-based command dispatch."""
    parser = argparse.ArgumentParser(
        description="Simple Task Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  py cli.py add "Buy groceries"
  py cli.py list
  py cli.py toggle 1
  py cli.py delete 1
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    
    # list command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    
    # toggle command
    toggle_parser = subparsers.add_parser("toggle", help="Toggle task completion status")
    toggle_parser.add_argument("id", type=int, help="Task ID")
    
    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize service
    service = TaskService()
    
    # Dispatch command to appropriate handler
    command_handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "toggle": cmd_toggle,
        "delete": cmd_delete,
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        handler(args, service)


if __name__ == "__main__":
    main()
