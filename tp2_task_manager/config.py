"""
Configuration module for Task Manager.
"""

import os
from typing import Final

# Application settings
APP_NAME: Final[str] = "Task Manager"
APP_VERSION: Final[str] = "1.0.0"

# Storage settings
STORAGE_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE: Final[str] = os.path.join(STORAGE_DIR, "tasks.json")

# Logging settings
LOG_LEVEL: Final[str] = "INFO"
LOG_FILE: Final[str] = os.path.join(STORAGE_DIR, "app.log")

# UI Settings
MENU_WIDTH: Final[int] = 40
TASK_LIST_WIDTH: Final[int] = 60

# Task status constants
STATUS_PENDING: Final[str] = "pending"
STATUS_COMPLETED: Final[str] = "completed"

# Date format
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
