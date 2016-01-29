__author__ = 'Nathalie'

import sqlite3
from time import time, strftime, gmtime
from os import path
from contextlib import closing

from tracker import TP_TODAY, TP_THIS_MONTH, TP_THIS_WEEK, TP_YESTERDAY

DB_NAME = 'ttdb.sqlite'

def prepare_db():
    if not path.isfile(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        with closing(conn.cursor()) as cur:
            cur.executescript('''
            CREATE TABLE tasks (
	            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	            task_name	TEXT UNIQUE );

            CREATE TABLE time_logs (
	            task_id	INTEGER NOT NULL,
	            start_time	INTEGER,
	            stop_time	INTEGER,
	            total_time	INTEGER );

	        CREATE INDEX index_start_time ON time_logs (start_time);

	        CREATE TABLE saved_states (
	            var	TEXT UNIQUE,
	            val	TEXT );

            ''')
        conn.commit()
        conn.close()


def init_db():
    return retrieve_tasks(), retrieve_saved_states()


def retrieve_tasks():
    conn = sqlite3.connect(DB_NAME)
    with closing(conn.cursor()) as cur:
        cur.execute('''select id, task_name from tasks;''')
        res = cur.fetchall()
    conn.close()
    return dict(res)


def retrieve_saved_states():
    conn = sqlite3.connect(DB_NAME)
    with closing(conn.cursor()) as cur:
        cur.execute('''select var, val from saved_states;''')
        res = cur.fetchall()
    conn.close()
    return dict(res)

def save_cur_state(vars):
    conn = sqlite3.connect(DB_NAME)
    with closing(conn.cursor()) as cur:
        for pair in vars:
            cur.execute('''insert or replace into saved_states (var, val) values
                       ( (select var from saved_states where var = ?), ?)''', (pair[0], pair[1]))
    conn.commit()
    conn.close()
    # 'last_task_id', str(self.current_task_id))

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
