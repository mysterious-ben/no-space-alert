"""
Provides functions to create loggers.
"""

from logutil import get_loguru_logger, init_loguru

from src import config


def init_logger():
    init_loguru(
        fmt=(f"{config.UNIQUE_ID} " + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {level}: {message}"),
        level="DEBUG",
        file_on=True,
        file_path=config.ROOT_PATH / "logs" / "logs.log",
        file_fmt=(
            f"{config.UNIQUE_ID} " + "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {level}: {message}"
        ),
        file_rotation=config.LOG_ROTATION,
        file_retention=1,
        file_level=config.LOG_FILE_LEVEL,
        pushover_on=config.PUSHOVER_ON,
        pushover_user=config.PUSHOVER_USER,
        pushover_token=config.PUSHOVER_TOKEN,
        pushover_level="WARNING",
        slack_on=config.SLACK_ON,
        slack_webhook_url=config.SLACK_WEBHOOK_URL,
        slack_level="WARNING",
        sentry_on=config.SENTRY_ON,
        sentry_dsn=config.SENTRY_DSN,
        sentry_breadcramp_level="DEBUG",
        sentry_event_level="WARNING",
    )


logger = get_loguru_logger()
