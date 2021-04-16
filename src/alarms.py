import time

import psutil
import schedule

from src import config
from src.log import init_logger, logger

init_logger()


def send_alarm_warning(space_left):
    logger.warning(f"Only {space_left:.2f} GB left!")


def send_alarm_error(space_left):
    logger.error(f"Only {space_left:.2f} GB left!")


def check_hdd():
    hdd = psutil.disk_usage(config.MOUNT_PATH)
    free_gb = hdd.free / (1024 * 1024 * 1024)
    if (free_gb > config.SPACE_LIMIT_ERROR) and (free_gb <= config.SPACE_LIMIT_WARNING):
        send_alarm_warning(free_gb)
    elif free_gb <= config.SPACE_LIMIT_ERROR:
        send_alarm_error(free_gb)
    else:
        logger.info(f"{free_gb:.2f} GB are free")


def start():
    schedule.every(config.CHECK_PERIOD).seconds.do(check_hdd)

    while True:
        schedule.run_pending()
        time.sleep(0.1)
