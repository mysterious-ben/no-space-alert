import time

import psutil
import schedule

from dotenv import find_dotenv, load_dotenv
from envparse import env


load_dotenv(find_dotenv(".env"))

SPACE_LIMIT_WARNING: int = env.int("SPACE_LIMIT_WARNING")
SPACE_LIMIT_ERROR: int = env.int("SPACE_LIMIT_ERROR")
CHECK_PERIOD: int = env.int("CHECK_PERIOD")
MOUNT_PATH: str = env.str("MOUNT_PATH")


def send_alarm_warning(space_left):
    print(f"WARNING: Only {space_left:.2f} GB left!")


def send_alarm_error(space_left):
    print(f"ERROR: Only {space_left:.2f} GB left!")


def check_hdd():
    hdd = psutil.disk_usage(MOUNT_PATH)
    free_gb = hdd.free / (1024 * 1024 * 1024)
    if (free_gb > SPACE_LIMIT_ERROR) and (free_gb <= SPACE_LIMIT_WARNING):
        send_alarm_warning(free_gb)
    elif free_gb <= SPACE_LIMIT_ERROR:
        send_alarm_error(free_gb)
    else:
        print(f"{free_gb:.2f} GB are free")


schedule.every(CHECK_PERIOD).seconds.do(check_hdd)


while True:
    schedule.run_pending()
    time.sleep(0.1)
