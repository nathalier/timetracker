__author__ = 'Nathalie'


import sqlite3
from os import path
from contextlib import closing


DB_NAME = 'ttdb.sqlite'


def prepare_db():
    if not path.isfile(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        conn.executescript('''
        CREATE TABLE task (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            task_name	TEXT UNIQUE,
          /*  parent_task_id	INTEGER,
            category_id	INTEGER */);

        CREATE TABLE time_log (
            task_id	INTEGER NOT NULL,
            start_time	REAL,
            stop_time	REAL,
            total_time	REAL,
	        offline_logged	INTEGER);

        CREATE INDEX index_start_time ON time_logs (start_time);

        CREATE TABLE saved_state (
            var	TEXT UNIQUE,
            val	TEXT );

      /*  CREATE TABLE category (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            cat_name	TEXT UNIQUE );

        CREATE TABLE memo (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            memo	TEXT NOT NULL,
            time_log_id	INTEGER,
            task_id	INTEGER NOT NULL );*/

        ''')
        conn.commit()
        conn.close()


def init_db():
    return retrieve_tasks(), retrieve_saved_state()


def retrieve_tasks():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute('''select id, task_name from task;''').fetchall()
    conn.close()
    return dict(res)


def retrieve_saved_state():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute('''select var, val from saved_state;''').fetchall()
    conn.close()
    return dict(res)


def save_cur_state(vars):
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            for pair in vars:
                conn.execute('''insert or replace into saved_state (var, val) values
                       ( (select var from saved_state where var = ?), ?)''', (pair[0], pair[1]))
            # conn.commit()
    except sqlite3.IntegrityError:
        pass  # TODO show error message
    conn.close()
    # 'last_task_id' #TODO list of parameters name


def log_time(task_id, start_t, stop_t, total_t, offline_l = 0):
    conn = sqlite3.connect('ttdb.sqlite')
    try:
        with conn:
            conn.execute('''insert into time_log (task_id, start_time, stop_time, total_time, offline_logged)
                       values (?, ?, ?, ?, ?);''',
                    (task_id, start_t, stop_t, total_t, offline_l))
    except sqlite3.IntegrityError:
        pass  # TODO show error message
    conn.close()


def select_time(task_id, start_t, end_t):
    conn = sqlite3.connect('ttdb.sqlite')
    res = conn.execute('''select total_time from time_log where task_id = ? and start_time >= ? and start_time <= ?;''',
                (task_id, start_t, end_t)).fetchall()
    res_list = [x[0] for x in res]
    return sum(res_list)
