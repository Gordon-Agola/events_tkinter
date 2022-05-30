import sqlite3



conn = sqlite3.connect("events.db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, title text, venue text, date text, email text,dt datetime default current_timestamp)")
conn.commit()

conn.close()
