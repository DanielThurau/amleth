from broker import MQTTBroker
from config import EnvConfig
from database import Database
import logging
from mqtt_event_processor import MQTTEventProcessor
import os
import queue
import sys
import threading
from utils import setup_logging, log_starting_message


def start_mqtt_broker(broker, shutdown_flag):
    try:
        broker.loop_forever()
    except Exception:
        logging.exception("Critical error in MQTT thread, initiating shutdown.")
        shutdown_flag.set()


def process_events(processor, shutdown_flag):
    try:
        processor.loop_forever()
    except Exception:
        logging.exception("Critical error in processing thread, initiating shutdown.")
        shutdown_flag.set()


def main():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    env_file = f"{ROOT_DIR}/../data/.env"
    config = EnvConfig(env_file)

    setup_logging(config)
    log_starting_message()

    # Threading event to detect errors in threads and gracefully shutdown. This is simple
    # error handling for now (all exceptions are treated as unrecoverable events) but
    # this lays the groundwork and organization for more complex thread handling in the
    # future.
    shutdown_flag = threading.Event()

    event_queue = queue.Queue()
    database = Database(config)

    broker = MQTTBroker(event_queue, config)
    processor = MQTTEventProcessor(event_queue, database)

    mqtt_thread = threading.Thread(
        target=start_mqtt_broker,
        args=(
            broker,
            shutdown_flag,
        ),
    )
    processor_thread = threading.Thread(
        target=process_events,
        args=(
            processor,
            shutdown_flag,
        ),
    )

    mqtt_thread.daemon = True
    processor_thread.daemon = True

    mqtt_thread.start()
    processor_thread.start()

    try:
        while True:
            mqtt_thread.join(timeout=1)
            processor_thread.join(timeout=1)
            if (
                shutdown_flag.is_set()
                or not mqtt_thread.is_alive()
                or not processor_thread.is_alive()
            ):
                raise Exception(
                    "Shutdown triggered by thread error or manual interruption."
                )
    except Exception:
        logging.exception(f"Exiting due to error")
    finally:
        broker.disconnect()
        logging.info("Broker disconnected. Program shutting down.")
        sys.exit(1)


if __name__ == "__main__":
    main()
