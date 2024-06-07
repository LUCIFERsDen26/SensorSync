import paho.mqtt.client as mqtt
from datetime import datetime
import mysql.connector
import json
import os

# Define MQTT parameters
mqtt_broker = os.environ.get("MQTT_BROKER")
mqtt_port = int(os.environ.get("MQTT_PORT"))
mqtt_topic = os.environ.get("MQTT_TOPIC")
mqtt_username = os.environ.get("MQTT_USERNAME")
mqtt_password = os.environ.get("MQTT_PASSWORD")

# Define MySQL parameters
mysql_host = os.environ.get("MYSQL_HOST")
mysql_port = int(os.environ.get("MYSQL_PORT"))
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_database = os.environ.get("MYSQL_DATABASE")

# Define MQTT client callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    try:
        # Parse received message payload as JSON
        payload = json.loads(msg.payload.decode())
        
        # Extract required fields from the JSON payload
        current_time = datetime.now().strftime("%H:%M:%S")
        qindex = payload["QIndex"]
        state = payload["random state"]
        graphy = payload["GraphYval"]
        wavey = payload["WaveYval"]
        
        # Store extracted values in MySQL database
        cnx = mysql.connector.connect(user=mysql_user, password=mysql_password, host=mysql_host, port=mysql_port, database=mysql_database)

        cursor = cnx.cursor()
        query = "INSERT INTO MQTable (Time, GraphYval, WaveYval, QIndex, random_state) VALUES (%s, %s, %s, %s, %s)"
        data = (current_time, graphy, wavey, qindex, state)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Stored values in MySQL database")
        
    except ValueError:
        print("Received message payload is not valid JSON")

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

# Start MQTT client loop
client.loop_forever()
