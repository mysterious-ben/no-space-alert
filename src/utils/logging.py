"""
Provides functions to create loggers.
"""
from pathlib import Path

from logutil import get_loguru_logger, init_loguru


ROOT_PATH: Path = Path(__file__).absolute().parent.parent.parent


def init_logger():
    init_loguru(
        fmt=(
            f"dev-local-avenon "
            + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {name} {level}: {message}"
        ),
        level="DEBUG",
        file_on=True,
        file_path=ROOT_PATH / "logs" / "logs",
        file_fmt=(
            f"dev-local-avenon "
            + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {name} {level}: {message}"
        ),
        file_rotation="50 MB",
        file_retention=1,
        pushover_on=False,
        pushover_user="",
        pushover_token="",
        pushover_level="WARNING",
        sentry_on=False,
        sentry_dsn="",
        sentry_breadcramp_level="DEBUG",
        sentry_event_level="WARNING",
    )


logger = get_loguru_logger()
