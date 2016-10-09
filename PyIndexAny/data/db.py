__author__ = 'Wei Wang'

import sqlite3


DB_FILE = "bc_data.db"
MAIN_TBL = "main"
mydb_conn = None


def prepare_db():
    if not exist_main_table():
        create_main_table()
    else:
        drop_main_table()
        create_main_table()


def drop_main_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.executescript("drop table if exists %s" % MAIN_TBL)
    conn.close()


def create_main_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE %s
        (   media_id INTEGER PRIMARY KEY autoincrement not null,
            file_path text,
            width INTEGER,
            height INTEGER,
            duration INTEGER,
            mtime_begin INTEGER,
            mtime_end INTEGER,
            nominal_date text,
            media_type text,
            is_compressed text,
            equipment text,
            location text,
            file_ext text
        )''' % MAIN_TBL)  # insecure, but binding does not work on table names..
    conn.commit()
    conn.close()


def exist_main_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    param = (MAIN_TBL,)
    c.execute('SELECT * FROM sqlite_master WHERE type="table" AND name=?'
              , param)
    ret = c.fetchall()
    return ret


def connect_db():
    global mydb_conn
    mydb_conn = sqlite3.connect(DB_FILE)


def close_db():
    mydb_conn.close()


def insert_stream(s_file):
    cur = mydb_conn.cursor()
    cur.execute('''INSERT INTO %s
    (file_path, width, height, duration, mtime_begin, mtime_end, nominal_date,
    media_type, is_compressed, equipment, location, file_ext )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                % MAIN_TBL, (s_file.file_path, s_file.video_width,
                             s_file.video_height, s_file.duration, s_file.mtime_begin,
                             s_file.mtime_end, s_file.nominal_date, s_file.media_type,
                             s_file.is_compressed, s_file.equipment, s_file.location,
                             s_file.ext))
    mydb_conn.commit()



