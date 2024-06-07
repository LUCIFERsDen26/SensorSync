FROM python:3.10

WORKDIR /app

RUN pip install paho-mqtt
RUN pip install mysql-connector-python

COPY mqtt-json-docker.py .

# Set environment variables for MQTT and MySQL
ENV MQTT_BROKER="192.168.73.199"
ENV MQTT_PORT="6677"
ENV MQTT_TOPIC="ESP/SyntheticDataGenI"
ENV MQTT_USERNAME="lucifer"
ENV MQTT_PASSWORD="123456789"

ENV MYSQL_HOST="127.0.0.1"
ENV MYSQL_PORT="3307"
ENV MYSQL_USER="esp"
ENV MYSQL_PASSWORD="123456789"
ENV MYSQL_DATABASE="MQTT"

CMD [ "python", "./mqtt-json-docker.py"]
