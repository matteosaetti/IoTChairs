#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Nome della tua rete WiFi";
const char* password = "Password della tua rete WiFi";

const char* mqtt_server = "192.168.18.10";
const char* clientID = "ESP32Client";

const int temperatureSensorPin = A0; 
const int lightSensorPin = T1;       
const int lightPin1 = 5;             
const int lightPin2 = 4;             

const int temperatureThreshold = 25; 
const int lightThreshold = 500;      

WiFiClient espClient;
PubSubClient client(espClient);

void connectWiFi() {
  Serial.println("Connessione alla rete WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connessione in corso...");
  }
  Serial.println("Connessione WiFi stabilita");
}

void callback(char* topic, byte* payload, unsigned int length) {
  if (strcmp(topic, "pressure_status") == 0) {
    if (payload[0] == 1) {
      int temperatureValue = analogRead(temperatureSensorPin);
      int lightValue = analogRead(lightSensorPin);

      if (temperatureValue < temperatureThreshold && lightValue < lightThreshold) {
        digitalWrite(lightPin1, HIGH);
        digitalWrite(lightPin2, HIGH);
      }
    } else {
      digitalWrite(lightPin1, LOW);
      digitalWrite(lightPin2, LOW);
    }
  }
}

void connectMQTT() {
  client.setCallback(callback);

  Serial.print("Connessione al server MQTT ");
  while (!client.connected()) {
    Serial.print("...");
    if (client.connect(clientID)) {
      Serial.println("Connesso al server MQTT");
      // Iscrizione al topic di interesse
      client.subscribe("pressure_status");
    } else {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(lightPin1, OUTPUT);
  pinMode(lightPin2, OUTPUT);

  connectWiFi();

  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

void loop() {
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();
}
