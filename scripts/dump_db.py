import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(f"{ROOT_DIR}/../data/application.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM power")
print(res.fetchall())

con.close()
