__author__ = 'Nathalie'

import sqlite3


def retrieve_tasks():
    conn = sqlite3.connect('ttdb.sqlite')
    cur = conn.cursor()

    cur.execute('''select task_name from tasks;''')
    return [x[0] for x in cur.fetchall()]

