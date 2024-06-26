#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "nome wifi";
const char* password = "password wifi";

const char *mqtt_broker = "ip computer";
const char *topic = "pressure_status";
const char *mqtt_username = "usr";
const char *mqtt_password = "";
const int mqtt_port = 1883;    

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

//void callback(char* topic, byte* payload, unsigned int length) {
//  if (strcmp(topic, "pressure_status") == 0) {
//    if (payload[0] == 1) {
//      int temperatureValue = analogRead(temperatureSensorPin);
//      int lightValue = analogRead(lightSensorPin);
//
//      if (temperatureValue < temperatureThreshold && lightValue < lightThreshold) {
//        digitalWrite(lightPin1, HIGH);
//        digitalWrite(lightPin2, HIGH);
//      }
//    } else {
//      digitalWrite(lightPin1, LOW);
//      digitalWrite(lightPin2, LOW);
//    }
//  }
//}

void connectMQTT() {
  client.setCallback(callback);

  Serial.print("Connessione al server MQTT ");
  while (!client.connected()) {
    Serial.print("...");
    if (client.connect(clientID)) {
      Serial.println("Connesso al server MQTT");
      client.subscribe("pressure_status");
    } else {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

//void setup() {
//  Serial.begin(115200);
//
//  pinMode(lightPin1, OUTPUT);
//  pinMode(lightPin2, OUTPUT);
//
//  connectWiFi();
//
//  client.setServer(mqtt_server, 1883);
//  connectMQTT();
//}
void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());


  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  connectMqtt();

  client.subscribe(topic);

}

int val = 0;
void loop() {
  int temp = analogRead(34);
  int light = analogRead(35);
  Serial.println(val++);
  if (val > 255) val = 0;
  delay(1000);
  if(!client.connected()){
    connectMqtt();
  }
  client.publish(temp_topic, String(temp).c_str());
  client.publish(light_topic, String(light).c_str());
  client.loop();
}