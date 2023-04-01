import paho.mqtt.client as mqtt
import os
import logging
from extractoor import configure_logging

configure_logging()

MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_USERNAME = os.environ['MQTT_USERNAME']
MQTT_PASSWORD = os.environ['API_KEY']


def on_connect(client, userdata, flags, rc):
    """Callback function for handling MQTT connection events.

    Args:
        client (mqtt.Client): Instance of the MQTT client calling the callback.
        userdata: Optional user data specified when creating the client instance.
        flags (dict): Dictionary containing response flags from the MQTT broker.
        rc (int): Connection result code. 0 indicates successful connection.
    """
    logging.info(f"Connected to MQTT broker with result code: {rc}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """Callback function for handling received MQTT messages.

    Args:
        client (mqtt.Client): Instance of the MQTT client calling the callback.
        userdata: Optional user data specified when creating the client instance.
        msg (mqtt.MQTTMessage): Instance of MQTTMessage containing message data.
    """
    logging.info(f"Received message on topic: {msg.topic}")
    logging.info(f"Message payload: {msg.payload.decode('utf-8')}")


def main():
    """Main function to start the MQTT client and handle callbacks."""

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
