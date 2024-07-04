#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "nome wifi";
const char* password = "password wifi";

const char* mqtt_server = "192.168.18.10";
const char* clientID = "ESP32Client2";
const char* topic = "sensor/pressure";

const int pressureSensorPin = A0; 
const int pressureThreshold = 500;

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

void connectMQTT() {
  client.setCallback(callback);

  Serial.print("Connessione al server MQTT ");
  while (!client.connected()) {
    Serial.print("...");
    if (client.connect(clientID)) {
      Serial.println("Connesso al server MQTT");
    } else {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

void loop() {
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();

  int pressureValue = analogRead(pressureSensorPin);

  String st = "";
  if (pressureValue > pressureThreshold) {
    st = String(topic) + "#2#1";
    client.publish(topic, st.c_str());
    Serial.println("1");
  } else {
    st = String(topic) + "#2#0";
    client.publish(topic, st.c_str());
    Serial.println("0");
  }
  }
  delay(500);
}