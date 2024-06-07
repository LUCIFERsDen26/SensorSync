# ESP8266 Synthetic Data Generator for MQTT

### This Arduino code generates and publishes synthetic data to an MQTT broker. 

- #### The data includes:

    - Air Quality Index (AQI): A random integer between 0 and 250.
    - Random Indian State: A random string representing a state in India.
    - Graph Data: Simulated values based on a sine wave with varying amplitude and frequency, along with added noise.
    - Waveform Data: Another simulated sine wave with varying amplitude and frequency, along with added noise.

### * The data is published as a JSON object to a specified MQTT topic.
### Hardware Requirements
- ESP8266 microcontroller board (e.g., NodeMCU, D1 Mini)
- Wi-Fi connection

### Software Requirements

- Arduino IDE (https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE)
- Adafruit MQTT library (https://github.com/adafruit/Adafruit_MQTT_Library)
- ArduinoJson library (https://github.com/bblanchon/ArduinoJson)

### Libraries

- #### The code includes the following libraries:

    - WiFi.h: Provides WiFi connection functionality.
    - PubSubClient.h: Enables communication with an MQTT broker.
    - ArduinoJson.h: Allows working with JSON data.
    - string.h: Provides string manipulation functions.

### Configuration

    - ssid          : Replace "Lucy" with your Wi-Fi network name.
    - password      : Replace "123456789" with your Wi-Fi network password.
    - mqtt_server   : Replace "192.168.73.199" with the IP address of your MQTT broker.
    - mqtt_user     : Replace "lucifer" with the username for your MQTT broker (if required).
    - mqtt_password : Replace "123456789" with the password for your MQTT broker (if required).
    - topic         : Replace "ESP/SyntheticDataGenI" with the desired topic name for publishing data.

### Code Explanation
- Setup:

    - 1. Initializes serial communication at 115200 baud rate.
    - 2. Connects to the specified Wi-Fi network.
    - 3. Sets up the MQTT client and connects to the broker.
    - 4. Initializes random number generation using analog read.
- Loop:

    - 1. Reconnects to the MQTT broker if disconnected.
    - 2. Generates synthetic data:
        - 1. Updates GraphAmplitude with random noise.
        - 2. Calculates GraphYval based on the sine wave equation.
        - 3. Generates a random AQI value.
        - 4. Selects a random Indian state using getRandomState.
        - 5. Generates random WaveAmplitude and WaveFrequency with noise.
        - 6. Calculates WaveYval based on the sine wave equation.
    - 3. Creates a JSON object containing the generated data.
    - 4. Serializes the JSON object to a string (payload).
    - 5. Prints the JSON payload to the serial monitor.
    - 6. Publishes the data to the MQTT topic.
    - 7. Waits for 200 milliseconds before the next loop iteration.
    - 8. reconnect:
    - 9. Attempts to reconnect to the MQTT broker until successful.
    - 10. getRandomState:
        - 1. Returns a random string from an array containing Indian state names.
    - 11. setup_wifi:
        - 1. Connects to the Wi-Fi network and prints the assigned IP address.

### Usage

- Install the required libraries in your Arduino IDE.
- Update the configuration parameters (ssid, password, etc.) with your values.
- Upload the code to your ESP8266 board.
- Open a serial monitor at 115200 baud to see the published data.
- Subscribe to the specified MQTT topic (ESP/SyntheticDataGenI) in your MQTT client to receive the data.

