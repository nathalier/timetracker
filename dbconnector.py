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
            name TEXT NOT NULL UNIQUE,
            parent_task_id	INTEGER,
            category_id	INTEGER /*NOT NULL*/);

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

        CREATE TABLE category (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name	TEXT NOT NULL UNIQUE );

        CREATE TABLE memo (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            memo	TEXT NOT NULL,
            time_log_id	INTEGER,
            task_id	INTEGER NOT NULL );

        ''')
        conn.commit()
        conn.close()


def retrieve_tasks():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute('''select t1.id, t1.name, t2.name, c.name
                          from task t1
                          left outer join task t2 on t1.parent_task_id = t2.id
                          left outer join category c on c.id = t1.category_id;''').fetchall()
    conn.close()
    return res


def get_tasks():
    tasks = retrieve_tasks()
    fntasks = compose_task_name(tasks)
    res = {}
    for task in tasks:
        cat_name = '' if task[3] is None else task[3]
        res[cat_name + '::' + fntasks[task[1]]] = task[0]
    return res


def compose_task_name(tasks):
    task_ptask = {}
    full_task_names = {}
    for task in tasks:
        task_ptask[task[1]] = task[2]
    for task in tasks:
        if task[1] not in full_task_names:
            full_task_names[task[1]] = task[1]
            parent, parents = task[1], []
            while parent is not None:
                parents.append(parent)
                parent = task_ptask[parent]
            prefix = ''
            for t in reversed(parents):
                full_task_names[t] = prefix + t
                prefix += t + '/'
    return full_task_names


def get_tasks_with_cat():
    tasks = retrieve_tasks()
    fntasks = compose_task_name(tasks)
    d_fullname_id, d_fullname_cat = {}, {}
    for task in tasks:
        d_fullname_id[fntasks[task[1]]] = task[0]
        d_fullname_cat[fntasks[task[1]]] = '' if task[3] is None else task[3]
    return d_fullname_id, d_fullname_cat


def retrieve_saved_state():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute('''select var, val from saved_state;''').fetchall()
    conn.close()
    return dict(res)


def retrieve_categories():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute('''select name, id from category;''').fetchall()
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
    except:
        import sys
        e = sys.exc_info()
        print(e) # TODO sqlite3.OperationalError
    conn.close()


def select_time(task_id, start_t, end_t):
    conn = sqlite3.connect('ttdb.sqlite')
    res = conn.execute('''select total_time from time_log where task_id = ? and start_time >= ? and start_time <= ?;''',
                (task_id, start_t, end_t)).fetchall()
    res_list = [x[0] for x in res]
    return sum(res_list)


def add_task(task_name, parent_task_id=None, category_id=None):
    success = False
    conn = sqlite3.connect('ttdb.sqlite')
    try:
        with conn:
            conn.execute('''insert into task(name, category_id, parent_task_id)
                       values (?, ?, ?);''',
                    (task_name, category_id, parent_task_id))
            success = True
    except sqlite3.IntegrityError:
        import sys
        e = sys.exc_info()
        print(e)  # TODO show error message
    conn.close()
    return success
