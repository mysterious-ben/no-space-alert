import time

import psutil
import schedule


def send_alarm_warning(space_left):
    print(f"WARNING: Only {space_left:.2f} GB left!")


def send_alarm_error(space_left):
    print(f"ERROR: Only {space_left:.2f} GB left!")


def check_hdd():
    hdd = psutil.disk_usage("/")
    free_gb = hdd.free / (1024 * 1024 * 1024)
    if (free_gb > 2) and (free_gb <= 3):
        send_alarm_warning(free_gb)
    elif free_gb <= 2:
        send_alarm_error(free_gb)
    else:
        print(f"{free_gb:.2f} GB are free")


schedule.every(5).seconds.do(check_hdd)


while True:
    schedule.run_pending()
    time.sleep(0.1)
