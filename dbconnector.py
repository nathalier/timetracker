__author__ = 'Nathalie'

import sqlite3


def pull_data():
    conn = sqlite3.connect('ttdb.sqlite')
    cur = conn.cursor()

    cur.execute('''select * from time_periods;''')
    time_periods = cur.fetchall()
    for row in time_periods:
        print(row[1])
