import paho.mqtt.client as mqtt
import logging
import schedule as sched
import time
import json
import os
from extractoor import get_earthquake_data, configure_logging

configure_logging()

MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_TOPIC = os.environ['MQTT_TOPIC']
MQTT_USERNAME = os.environ['MQTT_USERNAME']
MQTT_PASSWORD = os.environ['API_KEY']

# Keep track of published earthquake events
event_tracker = set()


def get_event_id(event):
    """Generate a unique identifier for an earthquake event based on its date, time, and location."""
    return f"{event['Date time']}_{event['Location']}"


def get_and_publish_data():
    """Retrieve earthquake data and publish new events."""
    try:
        earthquake_data = get_earthquake_data()
        new_events_published = False

        for event in earthquake_data:
            event_id = get_event_id(event)

            if event_id not in event_tracker:
                event_json = json.dumps(event)
                logging.info(f"Publishing event: {event_json}")
                mqtt_client.publish(MQTT_TOPIC, event_json)
                event_tracker.add(event_id)
                new_events_published = True

        if not new_events_published:
            logging.info("No new events")
        else:
            logging.info("New events published")

    except Exception as e:
        logging.error(f"Failed to retrieve and publish earthquake data: {e}")


def on_connect(client, userdata, flags, rc):
    mqtt_connack_rc_description = {
        0: "Connection Accepted",
        1: "Connection Refused, unacceptable protocol version",
        2: "Connection Refused, identifier rejected",
        3: "Connection Refused, server unavailable",
        4: "Connection Refused, bad user name or password",
        5: "Connection Refused, not authorized"
    }
    rc_description = mqtt_connack_rc_description.get(rc, "Unknown result code")
    logging.info(
        f"Connected to MQTT broker with result code: {rc} ({rc_description})")
    sched.every(30).seconds.do(get_and_publish_data)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
if MQTT_USERNAME and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
mqtt_client.loop_start()


def run_scheduler():
    while True:
        sched.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
