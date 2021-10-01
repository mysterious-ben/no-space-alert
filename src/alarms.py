import os
import time

import psutil
import schedule

from src import config
from src.log import init_logger, logger

init_logger()


def send_alarm_warning(gb_left: float, space_pct_left: float, mount_path: str):
    logger.warning(f"Only {gb_left:.2f}GB ({space_pct_left:.1f}%) left on '{mount_path}'!")


def send_alarm_error(space_left: float, space_pct_left: float, mount_path: str):
    logger.error(f"Only {space_left:.2f}GB ({space_pct_left:.1f}%) left on '{mount_path}'!")


def send_alarm_warning_inode(inode_left: int, inode_pct_left: float, mount_path: str):
    logger.warning(f"Only {inode_left:,} inodes ({inode_pct_left:.1f}%) left on '{mount_path}'!")


def send_alarm_error_inode(inode_left: int, inode_pct_left: float, mount_path: str):
    logger.error(f"Only {inode_left:,} inodes ({inode_pct_left:.1f}%) left on '{mount_path}'!")


def _check_hdd(mount_path: str):
    try:
        # Get disk space
        hdd = psutil.disk_usage(mount_path)
        free_space = hdd.free / (1024 * 1024 * 1024)
        total_space = hdd.total / (1024 * 1024 * 1024)
        free_space_pct = free_space / total_space * 100

        # Get disk inodes
        inode_hdd_mount = os.statvfs(mount_path)
        total_inode = inode_hdd_mount.f_files  # inodes
        free_inode = inode_hdd_mount.f_ffree  # free inodes
        free_inode_pct = free_inode / total_inode * 100
    except FileNotFoundError:
        logger.warning(f"failed to find '{mount_path}'")
    else:
        # Log and alert
        logger.info(
            f"space left on '{mount_path}': {free_space:.2f}GB ({free_space_pct:.1f}%) | inodes {free_inode:,} ({free_inode_pct:.1f}%)"
        )

        if (free_space_pct <= config.FREE_SPACE_PCT_WARNING) and (
            free_space_pct > config.FREE_SPACE_PCT_ERROR
        ):
            send_alarm_warning(free_space, free_space_pct, mount_path)
        elif free_space_pct <= config.FREE_SPACE_PCT_ERROR:
            send_alarm_error(free_space, free_space_pct, mount_path)

        if (free_inode_pct <= config.FREE_INODE_PCT_WARNING) and (
            free_inode_pct > config.FREE_INODE_PCT_ERROR
        ):
            send_alarm_warning_inode(free_inode, free_inode_pct, mount_path)
        elif free_inode_pct <= config.FREE_INODE_PCT_ERROR:
            send_alarm_error_inode(free_inode, free_inode_pct, mount_path)


def check_hdds():
    if len(config.MOUNT_PATHS) > 0:
        mount_paths = config.MOUNT_PATHS
    else:
        if len(config.FILE_SYSTEMS) > 0:
            fs_set = set(config.FILE_SYSTEMS)
            mount_paths = [
                p.mountpoint for p in psutil.disk_partitions(all=False) if p.fstype in fs_set
            ]
        else:
            mount_paths = [p.mountpoint for p in psutil.disk_partitions(all=False)]
    if len(mount_paths) > 0:
        logger.debug(f"monitoring {mount_paths}...")
    else:
        logger.warning("no disks to monitor!")
    for mount_path in mount_paths:
        _check_hdd(mount_path)


def start():
    logger.critical("free disk monitoring service started")
    schedule.every(config.CHECK_PERIOD_SECONDS).seconds.do(check_hdds)
    try:
        while True:
            schedule.run_pending()
            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit) as e:
        logger.debug(repr(e))
    except Exception as e:
        logger.error(repr(e))
    finally:
        logger.critical("free disk monitoring service ended")
        time.sleep(5)
