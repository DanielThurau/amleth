import os
import sqlite3

columns = [
    "id",
    "timestamp_ms",
    "power",
    "apparent_power",
    "reactive_power",
    "factor",
    "voltage",
    "current",
    "today_kWh",
    "yesterday_kWh",
    "kWh_diff",
    "emission_frequency_ms",
]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(f"{ROOT_DIR}/../data/application.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM power")
data = res.fetchall()

print(f"{columns[0]},{columns[1]},{columns[2]},{columns[3]},{columns[4]},{columns[5]},{columns[6]},{columns[7]},{columns[8]},{columns[9]},{columns[10]},{columns[11]}")
for row in data:
    print(
        f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]},{row[10]},{row[11]}"
    )

con.close()
