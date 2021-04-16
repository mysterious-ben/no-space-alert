from dotenv import find_dotenv, load_dotenv
from envparse import env

load_dotenv(find_dotenv(".env"))

# --- General
UNIQUE_ID: str = env.str("UNIQUE_ID")

# --- Alarms
SPACE_LIMIT_WARNING: int = env.int("SPACE_LIMIT_WARNING")
SPACE_LIMIT_ERROR: int = env.int("SPACE_LIMIT_ERROR")
CHECK_PERIOD: int = env.int("CHECK_PERIOD")
MOUNT_PATH: str = env.str("MOUNT_PATH")

# --- Pushover ---
PUSHOVER_ON: bool = env.bool("PUSHOVER_ON")
PUSHOVER_USER: str = env.str("PUSHOVER_USER")
PUSHOVER_TOKEN: str = env.str("PUSHOVER_TOKEN")

# --- Sentry ---
SENTRY_ON: bool = env.bool("SENTRY_ON")
SENTRY_DSN: str = env.str("SENTRY_DSN")
