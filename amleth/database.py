import logging
import os
import sqlite3

expected_columns = [
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


class Record:
    def __init__(
        self,
        timestamp_ms,
        power,
        apparent_power,
        reactive_power,
        factor,
        voltage,
        current,
        today_kWh,
        yesterday_kWh,
        kWh_diff,
        emission_frequency_ms,
    ):
        self.timestamp_ms = timestamp_ms
        self.power = power
        self.apparent_power = apparent_power
        self.reactive_power = reactive_power
        self.factor = factor
        self.voltage = voltage
        self.current = current
        self.today_kWh = today_kWh
        self.yesterday_kWh = yesterday_kWh
        self.kWh_diff = kWh_diff
        self.emission_frequency_ms = emission_frequency_ms


class Database:
    # TODO, given the multi-threading environment, its safer to
    # create a new connection everytime an event needs to be inserted.
    # This happens infrequently enough that I'm not ready to figure out
    # how I want to keep a single connection alive. In the future this
    # optimization may need to happen.
    def __init__(self, config):
        self.db_file = config.get("SQLITE_FILE")

        if not self.check_database_health():
            raise Exception("Database check failed.")

    def check_database_health(self):
        try:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                # Check if the 'power' table exists with the correct columns
                cur.execute(
                    "SELECT * FROM sqlite_master WHERE type='table' AND name='power'"
                )
                if cur.fetchone() is None:
                    logging.error("Table 'power' does not exist.")
                    return False

                # Check the schema of the 'power' table
                cur.execute("PRAGMA table_info('power')")
                columns = [row[1] for row in cur.fetchall()]
                if columns != expected_columns:
                    logging.error(
                        f"Schema of 'power' table does not match expected schema. Found: {columns}, Expected: {expected_columns}"
                    )
                    return False

                return True
        except sqlite3.Error:
            logging.exception(f"Database error")
            return False

    def insert(self, record):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            sql = """
            INSERT INTO power (timestamp_ms, power, apparent_power, reactive_power, factor, voltage, current, today_kWh, yesterday_kWh, kWh_diff, emission_frequency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                record.timestamp_ms,
                record.power,
                record.apparent_power,
                record.reactive_power,
                record.factor,
                record.voltage,
                record.current,
                record.today_kWh,
                record.yesterday_kWh,
                record.kWh_diff,
                record.emission_frequency_ms,
            )
            # Execute the query with the tuple of values
            cur.execute(sql, values)
            con.commit()
            logging.info(f"Committed SQL insert {values}")
