"""
定时爬取
"""
import time, sys, os
import schedule

sys.path.append(os.getcwd())

from db.dao.hostSpot import testAdd


def job():
    testAdd()
    print("爬取成功......")


schedule.every(1).seconds.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
