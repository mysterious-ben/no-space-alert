import os
import time
from datetime import datetime, timedelta, timezone
from typing import Dict

import psutil
import schedule

from src import config
from src.log import init_logger, logger

TIME_EPS = 0.1

init_logger()

hdd_reporters: Dict[str, Dict[str, "Reporter"]] = {}
ram_reporters: Dict[str, "Reporter"] = {}


def r_now() -> datetime:
    """Get current UTC datetime rounded to seconds"""
    now = datetime.now(tz=timezone.utc)
    return (now + timedelta(seconds=TIME_EPS)).replace(microsecond=0)


class Reporter:
    """Class to log measurements"""

    def __init__(
        self,
        warning_level: float,
        error_level: float,
        warning_inc: float,
        error_inc: float,
        msg_time_interval: int,
        alarm_time_interval: int,
        msg_template: str = "High resource usage level={level}",
    ) -> None:
        assert warning_level < error_level
        assert warning_inc >= 0
        assert error_inc >= 0
        assert alarm_time_interval >= 0
        self.warning_level = warning_level
        self.error_level = error_level
        self.warning_inc = warning_inc
        self.error_inc = error_inc
        self.alarm_time_interval = alarm_time_interval
        self.msg_time_interval = msg_time_interval
        self.msg_template = msg_template
        self._last_msg_time = r_now() - timedelta(seconds=1)
        self._next_msg_time = r_now()
        self._next_repeat_alarm_time = r_now()
        self._rolling_max_level = warning_level - warning_inc - 1

    def report_level(self, level: float, **kwargs):
        now = r_now()

        # 0 - nothing, 1 - info, 2 - warning, 3 - error
        report_code: int = 0

        if now >= self._next_msg_time:
            report_code = 1

        if level >= self.warning_level:
            level_change = level - self._rolling_max_level
            if (
                (now >= self._next_repeat_alarm_time)
                or ((level < self.error_level) and (level_change >= self.warning_inc))
                or ((level >= self.error_level) and (level_change >= self.error_inc))
                or (
                    (level < self.error_level)
                    and (level_change <= -self.warning_inc)
                    and (now >= self._next_msg_time)
                )
                or (
                    (level >= self.error_level)
                    and (level_change <= -self.error_inc)
                    and (now >= self._next_msg_time)
                )
            ):
                report_code = 2 if level < self.error_level else 3
                self._rolling_max_level = level

        msg = self.msg_template.format(level=level, **kwargs)
        if report_code == 0:
            logger.debug(msg)
        elif report_code == 1:
            logger.info(msg)
        elif report_code == 2:
            logger.warning(msg)
        elif report_code == 3:
            logger.error(msg)
        else:
            ValueError(f"{report_code=}")
        self._last_msg_time = now

        if now >= self._next_msg_time:
            self._next_msg_time += timedelta(seconds=self.msg_time_interval)
        if now >= self._next_repeat_alarm_time:
            self._next_repeat_alarm_time += timedelta(seconds=self.alarm_time_interval)


def init_hdd_reporters() -> None:
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
        logger.debug(f"init monitoring hdd disks {mount_paths}")
    else:
        logger.warning("no hdd disks to monitor!")
    for mount_path in mount_paths:
        hdd_reporters[mount_path] = {
            "space": Reporter(
                warning_level=config.HDD_SPACE_PCT_WARNING,
                error_level=config.HDD_SPACE_PCT_ERROR,
                warning_inc=config.HDD_WARNING_INC,
                error_inc=config.HDD_ERROR_INC,
                msg_time_interval=config.MIN_DELAY_SECONDS,
                alarm_time_interval=config.MAX_DELAY_SECONDS,
                msg_template=(
                    f"hdd space on '{mount_path}': "
                    + "used_pct={level:.1f} used_gb={used_space_gb:.2f} free_gb={free_space_gb:.2f}"
                ),
            ),
            "inode": Reporter(
                warning_level=config.HDD_INODE_PCT_WARNING,
                error_level=config.HDD_INODE_PCT_ERROR,
                warning_inc=config.HDD_WARNING_INC,
                error_inc=config.HDD_ERROR_INC,
                alarm_time_interval=config.MAX_DELAY_SECONDS,
                msg_time_interval=config.MIN_DELAY_SECONDS,
                msg_template=(
                    f"hdd inodes on '{mount_path}': "
                    + "used_pct={level:.1f} used={used_inode:,} free={free_inode:,}"
                ),
            ),
        }


def init_ram_reporters() -> None:
    logger.debug("init monitoring ram")
    ram_reporters["ram"] = Reporter(
        warning_level=config.HDD_INODE_PCT_WARNING,
        error_level=config.HDD_INODE_PCT_ERROR,
        warning_inc=config.HDD_WARNING_INC,
        error_inc=config.HDD_ERROR_INC,
        alarm_time_interval=config.MAX_DELAY_SECONDS,
        msg_time_interval=config.MIN_DELAY_SECONDS,
        msg_template=(
            "ram vm_used_pct={level:.1f} "
            + "swap_used_pct={swap_used_pct:.1f} "
            + "vm_used_gb={vm_used_gb:.2f} "
            + "vm_available_gb={vm_available_gb:.2f} "
            + "vm_free_gb={vm_free_gb:.2f} "
            + "vm_cached_gb={vm_cached_gb:.2f} "
            + "vm_buffers_gb={vm_buffers_gb:.2f} "
            + "vm_total_gb={vm_total_gb:.2f} "
            + "swap_free_gb={swap_free_gb:.2f} "
            + "swap_used_gb={swap_used_gb:.2f} "
            + "swap_total_gb={swap_total_gb:.2f}"
        ),
    )


def report_hdds():
    # logger.debug("report hdds load...")
    for mount_path, reporters in hdd_reporters.items():
        try:
            # Get disk space and inodes
            hdd = psutil.disk_usage(mount_path)
            inode = os.statvfs(mount_path)
        except FileNotFoundError:
            logger.error(f"failed to find '{mount_path}'")
        else:
            # Log and alert
            reporters["space"].report_level(
                level=(hdd.total - hdd.free) / hdd.total * 100,
                used_space_gb=(hdd.total - hdd.free) / (1024**3),
                free_space_gb=hdd.free / (1024**3),
            )
            reporters["inode"].report_level(
                level=(inode.f_files - inode.f_ffree) / inode.f_files * 100,
                used_inode=inode.f_files - inode.f_ffree,
                free_inode=inode.f_ffree,
            )


def report_ram():
    # logger.debug("report ram load...")
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    ram_reporters["ram"].report_level(
        level=(vm.total - vm.available) / vm.total * 100 if vm.total > 0 else 0,
        swap_used_pct=swap.used / swap.total * 100 if swap.total > 0 else 0,
        vm_available_gb=vm.available / (1024**3),
        vm_free_gb=vm.free / (1024**3),
        vm_used_gb=vm.used / (1024**3),
        vm_cached_gb=vm.cached / (1024**3),
        vm_buffers_gb=vm.buffers / (1024**3),
        vm_total_gb=vm.total / (1024**3),
        swap_used_gb=swap.used / (1024**3),
        swap_free_gb=swap.free / (1024**3),
        swap_total_gb=swap.total / (1024**3),
    )


def start():
    logger.critical("free disk monitoring service started")
    init_hdd_reporters()
    init_ram_reporters()
    schedule.every(config.CHECK_PERIOD_SECONDS).seconds.do(report_hdds)
    schedule.every(config.CHECK_PERIOD_SECONDS).seconds.do(report_ram)
    try:
        # while True:
        #     report_hdds()
        #     report_ram()
        #     time.sleep(config.CHECK_PERIOD_SECONDS)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit) as e:
        logger.debug(repr(e))
    except Exception as e:
        logger.error(repr(e))
    finally:
        logger.critical("free disk monitoring service ended")
        time.sleep(5)
