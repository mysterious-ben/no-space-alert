from pathlib import Path
from typing import List

from dotenv import find_dotenv, load_dotenv
from envparse import env

load_dotenv(find_dotenv(".env"))

# --- General
UNIQUE_ID: str = env.str("UNIQUE_ID")

# --- Alarms
FREE_SPACE_PCT_WARNING: float = env.float("FREE_SPACE_PCT_WARNING")
FREE_SPACE_PCT_ERROR: float = env.float("FREE_SPACE_PCT_ERROR")
FREE_INODE_PCT_WARNING: float = env.float("FREE_INODE_PCT_WARNING")
FREE_INODE_PCT_ERROR: float = env.float("FREE_INODE_PCT_ERROR")
CHECK_PERIOD_SECONDS: int = env.int("CHECK_PERIOD_SECONDS")
MOUNT_PATHS: List[str] = env.list("MOUNT_PATHS", subcast=str)
FILE_SYSTEMS: List[str] = env.list("FILE_SYSTEMS", subcast=str)

# --- Pushover ---
PUSHOVER_ON: bool = env.bool("PUSHOVER_ON")
PUSHOVER_USER: str = env.str("PUSHOVER_USER")
PUSHOVER_TOKEN: str = env.str("PUSHOVER_TOKEN")

# --- Sentry ---
SENTRY_ON: bool = env.bool("SENTRY_ON")
SENTRY_DSN: str = env.str("SENTRY_DSN")

# --- Paths ---
ROOT_PATH: Path = Path(__file__).absolute().parent.parent
