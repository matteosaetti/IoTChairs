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

void connectMqtt() {
  while (!client.connected()) {
    String client_id = "esp32-client-"+String(random(300));
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
        Serial.println("Public EMQX MQTT broker connected");
    } else {
        Serial.print("failed with state ");
        Serial.print(client.state());
        delay(2000);
    }
  }
}

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
  int press = analogRead(34);
  Serial.println(val++);
  if (val > 255) val = 0;
  delay(1000);
  if(!client.connected()){
    connectMqtt();
  }
  client.publish(press_topic, String(press).c_str())
  client.loop();
}
