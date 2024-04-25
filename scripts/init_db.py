import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(f"{ROOT_DIR}/../data/application.db")

cur = con.cursor()

res = cur.execute("SELECT name FROM sqlite_master")
if res.fetchone() is None:
    res = cur.execute(
        "CREATE TABLE power(id,timestamp,power,apparent_power,reactive_power,factor,voltage,current,today_kWh,yesterday_kWh)"
    )
    print("Creating 'power' table")
else:
    print("'power' table already exists")


con.close()
