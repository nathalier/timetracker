__author__ = 'Nathalie'


import sqlite3
from os import path
from timetracker import NULL_CAT
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

        CREATE INDEX index_start_time ON time_log (start_time);

        CREATE TABLE saved_state (
            var	TEXT UNIQUE,
            val	TEXT );

        CREATE TABLE category (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name	TEXT NOT NULL UNIQUE );

        CREATE TABLE memo (
            id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            memo	TEXT NOT NULL,
            time	REAL NOT NULL,
            task_id	INTEGER );

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
    conn.close()
    return sum(res_list)


def select_last_memo(task_id):
    conn = sqlite3.connect('ttdb.sqlite')
    res = conn.execute('''select memo, max(time) from memo where task_id = ?;''', (task_id, )).fetchone()
    conn.close()
    return res


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


def add_memo(memo_text, time, task_id=None):
    success = False
    conn = sqlite3.connect('ttdb.sqlite')
    try:
        with conn:
            conn.execute('''insert into memo(memo, time, task_id)
                       values (?, ?, ?);''',
                    (memo_text, time, task_id))
            success = True
    except sqlite3.IntegrityError:
        import sys
        e = sys.exc_info()
        print(e)  # TODO show error message
    conn.close()
    return success

def select_time_report(tp_start, tp_stop, cat_name, task_name,
                       flag_with_subtasks=False, flag_detailed=False, flag_cat_only=False):
    columns = ['Category', 'Task', 'Start', 'Stop', 'Spent Time', 'Manually']
    if flag_cat_only:
        columns.remove('Task')
    if not flag_detailed:
        columns.remove('Start')
        columns.remove('Stop')
        columns.remove('Manually')
    conn = sqlite3.connect('ttdb.sqlite')

    if flag_cat_only:
        if cat_name:
            if flag_detailed:
                res = conn.execute('''select c.name,
                                  datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                  time(tl.total_time, 'unixepoch'), tl.offline_logged
                                  from category c, task t, time_log tl
                                  where t.id == tl.task_id
                                  and t.category_id = c.id and c.name = ?
                                  and tl.start_time >= ? and tl.start_time < ?
                                  ORDER BY sorting;''', (cat_name, tp_start, tp_stop)).fetchall()
            else:
                res = conn.execute('''select c.name,
                                      time(sum(tl.total_time), 'unixepoch') sorting
                                      from category c, task t, time_log tl
                                      where t.id == tl.task_id
                                      and t.category_id = c.id and c.name = ?
                                      and tl.start_time >= ? and tl.start_time < ?
                                      ORDER BY sorting;''', (cat_name, tp_start, tp_stop)).fetchall()
        else:
            if cat_name == NULL_CAT:
                if flag_detailed:
                    res = conn.execute('''select '',
                                      datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                      time(tl.total_time, 'unixepoch'), tl.offline_logged
                                      from task t, time_log tl
                                      where t.category_id is NULL and t.id == tl.task_id
                                      and tl.start_time >= ? and tl.start_time < ?
                                      ORDER BY sorting;''', (tp_start, tp_stop)).fetchall()
                else:
                    res = conn.execute('''select '',
                                      time(sum(tl.total_time), 'unixepoch') sorting
                                      from task t, time_log tl
                                      where t.category_id is NULL and t.id == tl.task_id
                                      and tl.start_time >= ? and tl.start_time < ?
                                      ORDER BY sorting;''', (tp_start, tp_stop)).fetchall()
            else:
                if flag_detailed:
                    res = conn.execute('''select c.name,
                                  datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                  time(tl.total_time, 'unixepoch'), tl.offline_logged
                                  from time_log tl
                                  left outer join task t on tl.task_id = t.id
                                  left outer join category c on c.id = t.category_id
                                  where tl.start_time >= ? and tl.start_time < ?
                                  ORDER BY sorting;''', (tp_start, tp_stop)).fetchall()
                else:
                    res = conn.execute('''select c.name grouping1,
                                  time(sum(tl.total_time), 'unixepoch') sorting
                                  from time_log tl
                                  left outer join task t on tl.task_id = t.id
                                  left outer join category c on c.id = t.category_id
                                  where tl.start_time >= ? and tl.start_time < ?
                                  GROUP BY grouping1
                                  ORDER BY sorting DESC;''', (tp_start, tp_stop)).fetchall()
    else:
        if task_name:
            if flag_with_subtasks:
                pass
            else:
                # TODO move to timetracker.py
                start_pos = task_name.rfind('/') + 1
                trunc_task_name = task_name[start_pos:] if task_name.rfind('/') > 0 else task_name
                if flag_detailed:
                    res = conn.execute('''select c.name, t.name,
                                  datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                  time(tl.total_time, 'unixepoch'), tl.offline_logged
                                  from time_log tl
                                  left outer join task t on tl.task_id = t.id
                                  left outer join category c on c.id = t.category_id
                                  where t.name = ? and tl.start_time >= ? and tl.start_time < ?
                                  ORDER BY sorting;''', (trunc_task_name, tp_start, tp_stop)).fetchall()
                else:
                    res = conn.execute('''select c.name, t.name,
                                  time(sum(tl.total_time), 'unixepoch') sorting
                                  from time_log tl
                                  left outer join task t on tl.task_id = t.id
                                  left outer join category c on c.id = t.category_id
                                  where t.name = ? and tl.start_time >= ? and tl.start_time < ?
                                  ORDER BY sorting;''', (trunc_task_name, tp_start, tp_stop)).fetchall()
        elif cat_name:
            if flag_detailed:
                res = conn.execute('''select c.name, t.name,
                              datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                              time(tl.total_time, 'unixepoch'), tl.offline_logged
                              from time_log tl
                              left outer join task t on tl.task_id = t.id
                              left outer join category c on c.id = t.category_id and tl.task_id = t.id
                              where c.name = ? and tl.start_time >= ? and tl.start_time < ?
                              ORDER BY sorting;''', (cat_name, tp_start, tp_stop)).fetchall()
            else:
                res = conn.execute('''select c.name, t.name grouping1,
                              time(sum(tl.total_time), 'unixepoch') sorting
                              from time_log tl
                              left outer join task t on tl.task_id = t.id
                              left outer join category c on c.id = t.category_id and tl.task_id = t.id
                              where c.name = ? and tl.start_time >= ? and tl.start_time < ?
                              GROUP BY grouping1
                              ORDER BY sorting DESC;''', (cat_name, tp_start, tp_stop)).fetchall()
        else:
            if cat_name == NULL_CAT:
                if flag_detailed:
                    res = conn.execute('''select '', t.name
                                  datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                  time(tl.total_time, 'unixepoch'), tl.offline_logged
                                  from time_log tl, task t
                                  where tl.task_id = t.id and t.category_id is NULL
                                  and tl.start_time >= ? and tl.start_time < ?
                                  ORDER BY sorting;''', (tp_start, tp_stop)).fetchall()
                else:
                    res = conn.execute('''select '', t.name grouping1,
                                  time(sum(tl.total_time), 'unixepoch') sorting
                                  from time_log tl, task t
                                  where tl.task_id = t.id and t.category_id is NULL
                                  and tl.start_time >= ? and tl.start_time < ?
                                  GROUP BY grouping1
                                  ORDER BY sorting DESC;''', (tp_start, tp_stop)).fetchall()
            else:
                if flag_detailed:
                    res = conn.execute('''select c.name, t.name,
                                      datetime(tl.start_time, 'unixepoch') sorting, datetime(tl.stop_time, 'unixepoch'),
                                      time(tl.total_time, 'unixepoch'), tl.offline_logged
                                      from time_log tl
                                      left outer join task t on tl.task_id = t.id
                                      left outer join category c on c.id = t.category_id and tl.task_id = t.id
                                      where tl.start_time >= ? and tl.start_time < ?
                                      ORDER BY sorting;''', (tp_start, tp_stop)).fetchall()
                else:
                    res = conn.execute('''select c.name sorting1, t.name grouping1,
                                  time(sum(tl.total_time), 'unixepoch') sorting2
                                  from time_log tl
                                  left outer join task t on tl.task_id = t.id
                                  left outer join category c on c.id = t.category_id and tl.task_id = t.id
                                  where tl.start_time >= ? and tl.start_time < ?
                                  GROUP BY grouping1
                                  ORDER BY sorting1, sorting2 DESC;''', (tp_start, tp_stop)).fetchall()
    # TODO SHOW msg if error
    conn.close()
    return columns, res