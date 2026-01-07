"""Configuration settings for task management automation."""

import os
from pathlib import Path

# Project paths (now in system/automation/ so go up 2 levels)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DAILY_DIR = PROJECT_ROOT / "work" / "daily"
MEETINGS_DIR = PROJECT_ROOT / "work" / "meetings"
TEMPLATES_DIR = PROJECT_ROOT / "system" / "templates"

# Template files
DAILY_TEMPLATE = TEMPLATES_DIR / "daily.md"
MEETING_TEMPLATE = TEMPLATES_DIR / "meeting-v2.md"

# Calendar settings
DEFAULT_TIMEZONE = "America/New_York"  # Adjust as needed
CALENDAR_NAME = "primary"

# Automation settings
DEFAULT_RUN_TIME = "07:00"  # 7 AM
CHECK_EXISTING_FILES = True

# File patterns
DAILY_FILE_PATTERN = "{date}.md"  # YYYY-MM-DD.md
MEETING_FILE_PATTERN = "{date}-{meeting_slug}.md"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "automation" / "automation.log"

def ensure_directories():
    """Ensure all required directories exist."""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "system" / "automation").mkdir(parents=True, exist_ok=True)

def get_project_root():
    """Get the project root directory."""
    return PROJECT_ROOT

