from datetime import datetime
import json
import logging
import paho.mqtt.client as mqtt


def str_2_json(json_str):
    data = json.loads(json_str)
    time_dt = datetime.fromisoformat(data["Time"])
    time_ms = int(time_dt.timestamp() * 1000)

    return {
        "timestamp_ms": time_ms,
        "power": data["ENERGY"]["Power"],
        "apparent_power": data["ENERGY"]["ApparentPower"],
        "reactive_power": data["ENERGY"]["ReactivePower"],
        "factor": data["ENERGY"]["Factor"],
        "voltage": data["ENERGY"]["Voltage"],
        "current": data["ENERGY"]["Current"],
        "today_kWh": data["ENERGY"]["Today"],
        "yesterday_kWh": data["ENERGY"]["Yesterday"],
    }


class MQTTBroker:
    def __init__(self, queue, config):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.queue = queue
        self.topic = config.get("MQTT_BROKER_TOPIC")
        self.setup(config)

    def setup(self, config):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        username = config.get("MQTT_BROKER_USERNAME")
        password = config.get("MQTT_BROKER_PASSWORD")
        self.client.username_pw_set(username, password)

        ip = config.get("MQTT_BROKER_IP_ADDRESS")
        port = int(config.get("MQTT_BROKER_PORT_NUM"))
        logging.info(f"Connecting to broker on {ip}:{port}...")
        self.client.connect(ip, port, 60)

    def on_connect(self, client, _userdata, _flags, reason_code, _properties):
        logging.info(f"Connected with result code: {reason_code}")
        client.subscribe(self.topic)
        logging.info(f"Subscribed to topic: {self.topic}")

    def on_message(self, _client, _userdata, msg):
        json_msg = str_2_json(msg.payload)
        logging.debug(f"Received message: {json_msg}")
        self.queue.put(json_msg)

    def loop_forever(self):
        self.client.loop_forever()

    def disconnect(self):
        self.client.disconnect()
