import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(f"{ROOT_DIR}/../data/application.db")

cur = con.cursor()

res = cur.execute("SELECT name FROM sqlite_master")
if res.fetchone() is None:
    # TODO, it would nice for this not to be a huge string and be consistent with the schema used in the amleth app
    res = cur.execute(
        "CREATE TABLE power(id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp_ms,power,apparent_power,reactive_power,factor,voltage,current,today_kWh,yesterday_kWh, kWh_diff, emission_frequency_ms)"
    )
    print("Creating 'power' table")
else:
    print("'power' table already exists")


con.close()
