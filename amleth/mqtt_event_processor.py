from database import Record
import logging

"""
Through experimentation and observation, it appears that the
telemetry events are consistently emitted within +/- 1,000
milliseconds of their emission frequency. To give some extra
wiggle room, the acceptable delta between timestamps of the
same emission frequency, use this delta
"""
acceptable_timestamp_delta_ms = 2_500

"""
How often the TASMOTA plug emits telemetry data. Used for error 
detection.
"""
# TODO (low-priority): Automatically detect what the emission frequency is
emission_frequency_ms = 30_000


class MQTTEventProcessor:
    """
    Processes an MQTT event emitted from the MQTT Broker into a Record, and inserts it into a
    Database. This is all bespoke, and certainly won't scale, but for now, this works just fine
    and only needs a rewrite if I start manipulating the record anymore. Future
    considerations will standardize the `Record` class and have a generalized "bus" that
    Processors "listen" on. The database insertion should be at the end of the "bus".
    """

    def __init__(self, queue, database):
        self.queue = queue
        self.database = database

    def loop_forever(self):
        # Local variables used to cheaply track differences between records
        previous_event_timestamp_ms = 0
        previous_today_kWh = 0
        previous_yesterday_kWh = 0
        kWh_diff = 0

        while True:
            if not self.queue.empty():
                event = self.queue.get(timeout=10)
                if event is None:
                    logging.error(f"Event is somehow None...")
                    continue

                logging.debug(f"Processing event: {event}")

                if previous_event_timestamp_ms != 0:
                    current_time_diff = (
                        event["timestamp_ms"] - previous_event_timestamp_ms
                    )
                    logging.debug(f"current_time_diff={current_time_diff}")
                    if (
                        abs(current_time_diff - emission_frequency_ms)
                        <= acceptable_timestamp_delta_ms
                    ):
                        logging.debug(f"qualifies for computing power difference")
                        if event["yesterday_kWh"] == previous_yesterday_kWh:
                            kWh_diff = event["today_kWh"] - previous_today_kWh
                        else:
                            kWh_diff = event["today_kWh"]

                    else:
                        # TODO automatically alert when this error occurs.
                        logging.error(
                            f"Difference between events is outside of acceptable time delta {emission_frequency_ms}, "
                            f"resetting power diff calculation"
                        )
                        previous_today_kWh = 0
                        previous_yesterday_kWh = 0
                        kWh_diff = 0

                previous_today_kWh = event["today_kWh"]
                previous_yesterday_kWh = event["yesterday_kWh"]
                previous_event_timestamp_ms = event["timestamp_ms"]

                record = Record(
                    event["timestamp_ms"],
                    event["power"],
                    event["apparent_power"],
                    event["reactive_power"],
                    event["factor"],
                    event["voltage"],
                    event["current"],
                    event["today_kWh"],
                    event["yesterday_kWh"],
                    kWh_diff,
                    emission_frequency_ms,
                )

                self.database.insert(record)
                self.queue.task_done()
