import os
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


def send_alarm_warning_inode(inode_left):
    logger.warning(f"{inode_left:.0f} percents inode is used")


def send_alarm_error_inode(inode_left):
    logger.error(f"{inode_left:.0f} percents inode is used")


def check_hdd():
    inode_hdd_mount = os.statvfs(config.MOUNT_PATH)
    total_inode = inode_hdd_mount.f_files  # inodes
    free_inode = inode_hdd_mount.f_ffree  # free inodes
    used_inode = total_inode - free_inode  # used inodes
    inode_used_percentage = used_inode * 100 / total_inode
    hdd = psutil.disk_usage(config.MOUNT_PATH)
    free_gb = hdd.free / (1024 * 1024 * 1024)
    if (free_gb > config.SPACE_LIMIT_ERROR) and (free_gb <= config.SPACE_LIMIT_WARNING):
        send_alarm_warning(free_gb)
    elif free_gb <= config.SPACE_LIMIT_ERROR:
        send_alarm_error(free_gb)
    else:
        logger.info(f"{free_gb:.2f} GB are free")
    if (inode_used_percentage < config.SPACE_LIMIT_ERROR_INODE) and (
        inode_used_percentage >= config.SPACE_LIMIT_WARNING_INODE
    ):
        send_alarm_warning_inode(inode_used_percentage)
    elif inode_used_percentage >= config.SPACE_LIMIT_ERROR_INODE:
        send_alarm_error_inode(inode_used_percentage)
    else:
        logger.info(
            f"Total inode is {total_inode}. Used inode is {used_inode}. Percents used inode is {inode_used_percentage:.0f}%"
        )


def start():
    schedule.every(config.CHECK_PERIOD).seconds.do(check_hdd)

    while True:
        schedule.run_pending()
        time.sleep(0.1)
