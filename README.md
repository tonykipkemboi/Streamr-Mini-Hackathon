# 🌍 Real-Time Earthquake Monitoring 🚨

Check out the real-time (30 seconds refresh => `sched.every(30).seconds.do(get_and_publish_data)`
)) stream deployed [here](https://streamr.network/streams/0x4a2a3501e50759250828acd85e7450fb55a10a69%2Fearthquakes)!

## 📝 Overview

This project provides a real-time monitoring system for earthquake events using data from the EMSC (European-Mediterranean Seismological Centre) RSS feed. The system retrieves earthquake data, processes it, and streams it to a Streamr node using MQTT. Users can subscribe to the Streamr node to receive real-time updates on earthquake events as they happen.

## 🚀 Why Streamr?

Streamr enables efficient and secure data transfer, making it suitable for disseminating critical information such as earthquake data.

## 📊 Features

- Retrieves real-time earthquake data from the EMSC RSS feed.
- Processes and enriches earthquake data (e.g., magnitude scale description).
- Publishes earthquake events to a Streamr node using MQTT in real-time.
- Avoids publishing duplicate data for the same earthquake event.
- Modular code structure with separate modules for data extraction and publishing.

## 📁 Project Structure

- **publisher.py**: The publisher script collects earthquake data from the data source, processes it, and publishes it to the Streamr stream.
- **subscriboor.py**: The subscriber script subscribes to the Streamr stream and receives real-time updates on earthquake events.
- **Dockerfile**: Dockerfile for building the Docker images for the publisher and subscriber.
- **docker-compose.yml**: Docker Compose file for deploying the application on Docker.

## 🔗 Streamr Integration

The integration of Streamr technology is implemented in the `publisher.py` and `subscriboor.py` files. The `publisher.py` script uses the Streamr `MQTT broker` to publish earthquake data to the Streamr stream. The `subscriboor.py` script uses the Streamr `MQTT broker` to subscribe to the stream and receive real-time updates.

## 🐍 Code Snippet

In `publisher.py`, the following code snippet shows how to publish data to the Streamr stream using the MQTT client:

```bash
def get_and_publish_data():
    earthquake_data = get_earthquake_data()
    for event in earthquake_data:
        mqtt_client.publish(MQTT_TOPIC, event_json)
mqtt_client.connect(MQTT_HOST, MQTT_PORT)
mqtt_client.loop_start()
```

In `subscriboor.py`, the following code snippet shows how to subscribe to the Streamr stream using the MQTT client:

```bash
def on_message(client, userdata, msg):
    logging.info(f"Received message on topic: {msg.topic}")
    logging.info(f"Message payload: {msg.payload.decode('utf-8')}")

def main():
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()
```

## 🧰 Requirements

- Python 3.7 or higher
- Docker
- Libraries: `requests`, `beautifulsoup4`, `pandas`, `paho-mqtt`, `schedule`, `pytz`
- Access to a Streamr node (with MQTT plugin enabled)

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/tonykipkemboi/Streamr-Mini-Hackathon.git
```

2. Change into the project directory:

```bash
cd Streamr-Mini-Hackathon
```

3. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ How to Run

1. Configure the MQTT connection details in `publisher.py` (MQTT_HOST and MQTT_TOPIC).

2. Set up environment variables in a `.env` file based on the `.env.example` file.

3. Build the Docker images using the command `docker-compose build`.

4. Run the Docker containers using the command `docker-compose up`.

## 🚀 Deployment to DigitalOcean

The earthquake data streaming service has been deployed to a DigitalOcean Droplet. The Droplet is set up as an MQTT broker to which the publisher script (publisher.py) publishes new earthquake events, and the subscriber script (subscriboor.py) subscribes to receive the events. Both the publisher and subscriber scripts run as Docker containers on the Droplet.

## 📜 License

This project is licensed under the MIT [License](LICENSE).

## 📣 Acknowledgments

- Data Source: [EMSC Earthquake RSS Feed](https://www.emsc-csem.org/service/rss/rss.php?typ=emsc)
- MQTT Library: [Paho MQTT](https://pypi.org/project/paho-mqtt/)
- Streamr: [Streamr Network](https://www.streamr.network/)

## 📫 Contact

- Twitter: [tonykipkemboi](https://www.twitter.com/tonykipkemboi)
- GitHub: [tonykipkemboi](https://github.com/tonykipkemboi)
