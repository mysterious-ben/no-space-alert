import os
import time

import psutil
import schedule

from src import config
from src.log import init_logger, logger

init_logger()


def send_alarm_warning(gb_left: float, space_pct_left: float):
    logger.warning(f"Only {gb_left:.2f}GB ({space_pct_left:.1f}%) left!")


def send_alarm_error(space_left: float, space_pct_left: float):
    logger.error(f"Only {space_left:.2f}GB ({space_pct_left:.1f}%) left!")


def send_alarm_warning_inode(inode_left: int, inode_pct_left: float):
    logger.warning(f"Only {inode_left:,} inodes ({inode_pct_left:.1f}%) left!")


def send_alarm_error_inode(inode_left: int, inode_pct_left: float):
    logger.error(f"Only {inode_left:,} inodes ({inode_pct_left:.1f}%) left!")


def check_hdd():
    # Get disk space
    hdd = psutil.disk_usage(config.MOUNT_PATH)
    free_space = hdd.free / (1024 * 1024 * 1024)
    total_space = hdd.total / (1024 * 1024 * 1024)
    free_space_pct = free_space / total_space * 100

    # Get disk inodes
    inode_hdd_mount = os.statvfs(config.MOUNT_PATH)
    total_inode = inode_hdd_mount.f_files  # inodes
    free_inode = inode_hdd_mount.f_ffree  # free inodes
    free_inode_pct = free_inode / total_inode * 100

    # Log and alert
    logger.info(
        f"Space left: {free_space:.2f}GB ({free_space_pct:.1f}%) | inodes {free_inode:,} ({free_inode_pct:.1f}%)"
    )

    if (free_space <= config.FREE_SPACE_PCT_WARNING) and (
        free_space > config.FREE_SPACE_PCT_ERROR
    ):
        send_alarm_warning(free_space, free_space_pct)
    elif free_space <= config.FREE_SPACE_PCT_ERROR:
        send_alarm_error(free_space, free_space_pct)

    if (free_inode_pct <= config.FREE_INODE_PCT_WARNING) and (
        free_inode_pct > config.FREE_INODE_PCT_ERROR
    ):
        send_alarm_warning_inode(free_inode_pct, free_inode_pct)
    elif free_inode_pct <= config.FREE_INODE_PCT_ERROR:
        send_alarm_error_inode(free_inode_pct, free_inode_pct)


def start():
    logger.critical("free disk monitoring service started")
    schedule.every(config.CHECK_PERIOD_SECONDS).seconds.do(check_hdd)
    try:
        while True:
            schedule.run_pending()
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit) as e:
        logger.debug(repr(e))
    except Exception as e:
        logger.error(repr(e))
    finally:
        logger.critical("free disk monitoring service ended")
        time.sleep(5)
