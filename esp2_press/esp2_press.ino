#include <WiFi.h>
#include <PubSubClient.h>

#define PRESSURE_THRESHOLD 500
//Wi-fi connection data
const char *ssid = "iPhone di saio";
const char *password = "ciaociao12";

//mqtt server connection data
const char *mqtt_server = "172.20.10.5";
const char *clientID = "ESP32Client2";

//topic
const char *topic = "sensor/pressure";

//ESP32 pin
const int pressureSensorPin = A0;

WiFiClient espClient;
PubSubClient client(espClient);


//Wi-fi connection function
void connectWiFi()
{
  Serial.println("Connessione alla rete WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connessione in corso...");
  }
  Serial.println("Connessione WiFi stabilita");
}

//callback function
void callback(char *topic, byte *payload, unsigned int length)
{
}

//Mqtt connection function
void connectMQTT()
{
  client.setCallback(callback);

  Serial.print("Connessione al server MQTT ");
  while (!client.connected())
  {
    Serial.print("...");
    if (client.connect(clientID))
    {
      Serial.println("Connesso al server MQTT");
    }
    else
    {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

//Setup function
void setup()
{
  Serial.begin(115200);
  connectWiFi();
  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

//Loop function with topic management + publish of pressure values
void loop()
{
  if (!client.connected())
  {
    connectMQTT();
  }
  client.loop();

  int pressureValue = analogRead(pressureSensorPin);

  String st = "";
  if (pressureValue > PRESSURE_THRESHOLD)
  {
    st = String(topic) + "#2#1";
    client.publish(topic, st.c_str());
    Serial.println("1");
  }
  else
  {
    st = String(topic) + "#2#0";
    client.publish(topic, st.c_str());
    Serial.println("0");
  }
delay(500);
}