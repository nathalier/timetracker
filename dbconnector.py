__author__ = 'Nathalie'

import sqlite3
from time import time, strftime, gmtime

from tracker import TP_TODAY, TP_THIS_MONTH, TP_THIS_WEEK, TP_YESTERDAY


def retrieve_tasks():
    cur = sqlite3.connect('ttdb.sqlite').cursor()
    cur.execute('''select id, task_name from tasks;''')
    res = cur.fetchall()
    cur.close()
    return res


def log_time(task_id, start_time, stop_time):
    conn = sqlite3.connect('ttdb.sqlite')
    cur = conn.cursor()
    cur.execute('''insert into time_logs (task_id, start_time, stop_time, start_day, total_time)
                   values (?, ?, ?, ?, ?);''',
                (task_id, start_time, stop_time, strftime('%Y-%m-%d', gmtime(start_time)), stop_time - start_time))
    conn.commit()
    cur.close()


def select_time(task_id, period_start=TP_TODAY, period_end=TP_TODAY):
    cur = sqlite3.connect('ttdb.sqlite').cursor()
    if period_start == TP_TODAY:
        start_day, end_day = strftime('%Y-%m-%d', gmtime()), strftime('%Y-%m-%d', gmtime())
    #     TODO
    cur.execute('''select total_time from time_logs where task_id = ? and start_day >= ? and start_day <= ?;''',
                (task_id, start_day, end_day))
    res = [x[0] for x in cur.fetchall()]
    cur.close()
    return sum(res)
