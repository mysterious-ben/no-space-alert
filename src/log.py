"""
Provides functions to create loggers.
"""
from pathlib import Path

from logutil import get_loguru_logger, init_loguru

from src import config

ROOT_PATH: Path = Path(__file__).absolute().parent.parent.parent


def init_logger():
    init_loguru(
        fmt=(f"{config.UNIQUE_ID} " + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {level}: {message}"),
        level="DEBUG",
        file_on=True,
        file_path=ROOT_PATH / "logs" / "logs.log",
        file_fmt=(
            f"{config.UNIQUE_ID} " + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {level}: {message}"
        ),
        file_rotation="50 MB",
        file_retention=1,
        pushover_on=config.PUSHOVER_ON,
        pushover_user=config.PUSHOVER_USER,
        pushover_token=config.PUSHOVER_TOKEN,
        pushover_level="WARNING",
        sentry_on=config.SENTRY_ON,
        sentry_dsn=config.SENTRY_DSN,
        sentry_breadcramp_level="DEBUG",
        sentry_event_level="WARNING",
    )


logger = get_loguru_logger()
