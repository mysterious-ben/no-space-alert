from pathlib import Path
from typing import List

from dotenv import find_dotenv, load_dotenv
from envparse import env

load_dotenv(find_dotenv(".env"))

# --- General
UNIQUE_ID: str = env.str("UNIQUE_ID")

# --- Alarms
HDD_SPACE_PCT_WARNING: float = env.float("HDD_SPACE_PCT_WARNING")
HDD_SPACE_PCT_ERROR: float = env.float("HDD_SPACE_PCT_ERROR")
HDD_INODE_PCT_WARNING: float = env.float("HDD_INODE_PCT_WARNING")
HDD_INODE_PCT_ERROR: float = env.float("HDD_INODE_PCT_ERROR")
HDD_WARNING_INC: float = env.float("HDD_WARNING_INC")
HDD_ERROR_INC: float = env.float("HDD_ERROR_INC")
RAM_PCT_WARNING: float = env.float("RAM_PCT_WARNING")
RAM_PCT_ERROR: float = env.float("RAM_PCT_ERROR")
RAM_WARNING_INC: float = env.float("RAM_WARNING_INC")
RAM_ERROR_INC: float = env.float("RAM_ERROR_INC")
CHECK_PERIOD_SECONDS: int = env.int("CHECK_PERIOD_SECONDS")
MAX_DELAY_SECONDS: int = env.int("MAX_DELAY_SECONDS")
MIN_DELAY_SECONDS: int = env.int("MIN_DELAY_SECONDS")
MOUNT_PATHS: List[str] = env.list("MOUNT_PATHS", subcast=str)
FILE_SYSTEMS: List[str] = env.list("FILE_SYSTEMS", subcast=str)
LOG_ROTATION: str = env.str("LOG_ROTATION")

# --- Pushover ---
PUSHOVER_ON: bool = env.bool("PUSHOVER_ON")
PUSHOVER_USER: str = env.str("PUSHOVER_USER")
PUSHOVER_TOKEN: str = env.str("PUSHOVER_TOKEN")

# --- Sentry ---
SLACK_ON: bool = env.bool("SLACK_ON")
SLACK_WEBHOOK_URL: str = env.str("SLACK_WEBHOOK_URL")

# --- Sentry ---
SENTRY_ON: bool = env.bool("SENTRY_ON")
SENTRY_DSN: str = env.str("SENTRY_DSN")

# --- Paths ---
ROOT_PATH: Path = Path(__file__).absolute().parent.parent
