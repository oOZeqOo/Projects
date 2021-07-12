import os
import time
import shutil
import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from vars.variables import *


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        organize_path_by_month_year(FOLDER_TO_TRACK)
        print(f"Completed Check of {FOLDER_TO_TRACK}")


def organize_path_by_month_year(file_path, limit=None):
    count = 0
    for file_name in os.listdir(file_path):
        full_path = os.path.join(file_path, file_name)
        print(full_path)

        if not os.path.isdir(full_path):
            file_creation_date = get_creation_date(full_path)

            new_location = os.path.join(file_path, file_creation_date)
            if not os.path.exists(new_location):
                os.makedirs(os.path.join(file_path, new_location))
                print(f"Created {full_path}")

            old_file_path = file_path + "/" + file_name
            new_file_path = new_location + "/" + file_name
            shutil.move(old_file_path, new_file_path)

            count += 1
            if limit is None:
                continue

            if count >= limit:
                break
    print(f"Moved {count} files to their respective directories")


def create_new_folder(folder_name):
    path = FOLDER_TO_TRACK + "/" + folder_name
    Path(path).mkdir(exist_ok=True)
    print("Created : ", path)


def get_folder_name():
    today = datetime.date.today()
    month = MONTHS[(int(today.month) - 1) % 12]
    year = str(today.year)
    return year + "_" + month


def get_creation_date(file_path):
    time_stamp = os.path.getmtime(file_path)
    print(" * ", time_stamp)
    new_date = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m").split("-")
    print(" * ", new_date)
    month = MONTHS[(int(new_date[1]) - 1) % 12]
    year = str(new_date[0])
    origin = year + "_" + month
    return origin


if __name__ == "__main__":
    print("Starting up...")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_TRACK, recursive=True)
    observer.start()
    print("Started Observer")
    try:
        while True:
            print(f"Sleeping for {SLEEP_TIME} seconds...")
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt as e:
        print(e)
        observer.stop()
    except Exception as e:
        print(e)
        observer.stop()
    observer.join()
