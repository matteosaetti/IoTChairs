#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid = "nome wifi";
const char *password = "password wifi";

const char *mqtt_server = "192.168.1.175";
const char *clientID = "ESP32Client3";

const char *topic_mode = "mode";
const char *topic_light = "sensor/light";
const char *topic_temp = "sensor/temp";
const char *topic_b_light = "buttons/light";
const char *topic_b_temp = "buttons/temp";
const char *topic_set_light = "settings/light";
const char *topic_set_temp = "settings/temp";

const int lightPin = 32;
const int heatPin = 33;
const int tempPin = A0;

WiFiClient espClient;
PubSubClient client(espClient);

float tempSet = 25.0;
float lightSet = 300;
bool lightOn = false;
bool heatOn = false;
bool mode = false;

int prevTemp = -1;
int prevLight = -1;

void callback(char *topic, byte *message, unsigned int length)
{
  String message_s;

  for (int i = 0; i < length; i++)
  {
    Serial.print((char)message[i]);
    message_s += (char)message[i];
  }
  Serial.println("Msg on topic: " + String(topic) + " --> " + message_s);

  if (String(topic) == topic_mode)
  {
    mode = message_s.toInt();
  }
  else if (String(topic) == topic_set_light)
  {
    lightSet = message_s.toInt();
  }
  else if (String(topic) == topic_set_temp)
  {
    tempSet = message_s.toFloat();
  }
  else if (String(topic) == topic_b_light)
  {
    // char* split = strtok(message_s.toCharArray(), "#");
    lightOn = (message_s.toInt() == 1);
  }
  else if (String(topic) == topic_b_temp)
  {
    // char* split = strtok(message_s.toCharArray(), "#");
    heatOn = (message_s.toInt() == 1);
  }
}

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

      client.subscribe(topic_mode);
      client.subscribe(topic_set_light);
      client.subscribe(topic_set_temp);
      client.subscribe(topic_b_light);
      client.subscribe(topic_b_temp);
    }
    else
    {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(heatPin, OUTPUT);
  pinMode(tempPin, INPUT);

  digitalWrite(lightPin, LOW);
  digitalWrite(heatPin, LOW);

  connectWiFi();
  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

void loop()
{
  if (!client.connected())
  {
    connectMQTT();
  }
  client.loop();

  int temp = analogRead(tempPin);
  int light = analogRead(lightPin);
  // TODO calcolare bene la temp
  Serial.println("temp: " + String(temp));
  Serial.println("light: " + String(light));

  if (!mode)
  {
    if (light < lightSet)
    {
      digitalWrite(lightPin, HIGH);
    }
    else
    {
      digitalWrite(lightPin, LOW);
    }

    if (temp < tempSet)
    {
      digitalWrite(heatPin, HIGH);
    }
    else
    {
      digitalWrite(heatPin, LOW);
    }
  }
  else
  {
    if (lightOn)
    {
      Serial.println("light on");
      digitalWrite(2, HIGH);
      digitalWrite(lightPin, HIGH);
    }
    else
    {
      Serial.println("light off");
      digitalWrite(lightPin, LOW);
    }
    if (heatOn)
    {
      Serial.println("temp on");
      digitalWrite(heatPin, HIGH);
    }
    else
    {
      Serial.println("temp off");
      digitalWrite(heatPin, LOW);
    }
  }
  if(light != prevLight){
    String stLight = String(topic_light) + "#" + light;
    client.publish(topic_light, stLight.c_str());
    prevLight = light;
  }
  if(temp != prevTemp){
    String stTemp = String(topic_temp) + "#" + temp;
    client.publish(topic_temp, stTemp.c_str());
    prevTemp = temp;
  }

  delay(500);
}
