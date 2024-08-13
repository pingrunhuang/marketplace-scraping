import csv
import datetime

def initialize_driver():
    pass


def save_csv(data, filepath, columns):
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)


def today(fmt:str="%Y-%m-%d")->str:
    dt = datetime.datetime.now()
    return dt.strftime(fmt)
