#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <string.h>

const char* ssid = "Lucy";
const char* password = "123456789";

const char* mqtt_server = "192.168.73.199";
const char* mqtt_user = "lucifer";
const char* mqtt_password = "123456789";

const char* topic = "ESP/SyntheticDataGenI";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;
 
float GraphAmplitude = random(5); // set initial amplitude of sine wave
float GraphFrequency = 10; // set frequency of sine wave
float GraphNoise = 2; // set noise level


void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 6677);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (client.connect("ESP8266Client", mqtt_user, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  // Graph Genarater
  GraphAmplitude += GraphNoise * random(-100, 100) / 100.0; // add random noise to amplitude
  float GraphYval = GraphAmplitude * sin(GraphFrequency);
  
  
  // Air quality Index
  int qIndex = random(0, 250);
  
  
  // Random India State
  String randomState = getRandomState();
  
  
  // Random Waveform genrator
  float WaveAmplitude = random(1,5); // set initial amplitude of sine wave
  float WaveFrequency = random(1,5); // set frequency of sine wave
  float WaveNoise = random(0.1,2.5); // set noise level

  WaveAmplitude += WaveNoise * random(-100, 100) / 100.0; // add random noise to amplitude
  float WaveYval = WaveAmplitude * sin(WaveFrequency);

  
  // Create JSON object
  StaticJsonDocument<100> jsonDoc;
  jsonDoc["QIndex"] = qIndex;
  jsonDoc["random state"] = randomState;
  jsonDoc["GraphYval"] = GraphYval;
  jsonDoc["WaveYval"] = WaveYval;

  // Serialize JSON object to string
  String payload;
  serializeJson(jsonDoc, payload);

  Serial.print("Publishing message: ");
  // Output JSON string
  Serial.println(payload);    
  client.publish(topic, payload.c_str());
  
  client.loop();
  delay(200);
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe("esp8266/control");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}


String getRandomState() {
  String states[] = {
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
  };
  
  int numStates = sizeof(states) / sizeof(states[0]);
  int randomIndex = random(0, numStates);
  
  return states[randomIndex];
}

void setup_wifi() {
   delay(10);
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
   randomSeed(analogRead(0));
   Serial.println("");
   Serial.println("WiFi connected");
   Serial.println("IP address: ");
   Serial.println(WiFi.localIP());
}
