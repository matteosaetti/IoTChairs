#include <WiFi.h>
#include <PubSubClient.h>

#define TEMP_RANGE 0.5
#define LIGHT_RANGE 20

//Wi-fi connection data
//const char *ssid = "iPhone di saio";
//const char *password = "ciaociao12";
//mqtt server connection data
const char *mqtt_server = "192.168.1.175";
//const char *mqtt_server = "172.20.10.5";
const char *clientID = "ESP32Client3";

//topics
const char *topic_mode = "mode";
const char *topic_pressure = "sensor/pressure";
const char *topic_light = "sensor/light";
const char *topic_temp = "sensor/temp";
const char *topic_b_light = "buttons/light";
const char *topic_b_temp = "buttons/temp";
const char *topic_set_light = "settings/light";
const char *topic_set_temp = "settings/temp";

//ESP32 sensors pin 
const int lightPin = 34;
const int heatPin = 35;
//ESP32 lights pin
const int tempPin = 33;
const int luxPin = 32;

WiFiClient espClient;
PubSubClient client(espClient);

float tempSet = 25.0;
float lightSet = 300;
bool lightOn = false;
bool heatOn = false;
bool mode = false;
bool pressure1 = false;
bool pressure2 = false;

int prevTemp = -1;
int prevLight = -1;

//callback function for subscribed topics' management
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
    lightOn = (message_s.toInt() == 1);
  }
  else if (String(topic) == topic_b_temp)
  {
    heatOn = (message_s.toInt() == 1);
  }
    else if (String(topic) == topic_pressure)
  {
    if(message_s[0] == '1')
    {
        pressure1 = (message_s[2] == '1');
    }
    else if(message_s[0] == '2')
    {
        pressure2 = (message_s[2] == '1');
    }
  }
}

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

//Mqtt connection function + subscribe to topics
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
      client.subscribe(topic_pressure);
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

//Setup esp32 function
void setup()
{
  Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(heatPin, OUTPUT);
  pinMode(tempPin, INPUT);
  pinMode(luxPin, INPUT);

  digitalWrite(lightPin, LOW);
  digitalWrite(heatPin, LOW);

  connectWiFi();
  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

//Loop function with topics management + publish of temp and light values
void loop()
{
  if (!client.connected())
  {
    connectMQTT();
  }
  client.loop();

  int temp = analogRead(tempPin);
  int light = analogRead(luxPin);

  Serial.println("temp: " + String(temp));
  Serial.println("light: " + String(light));

  if (!mode && (pressure1 || pressure2))
  {
    if (light < lightSet)
    {
      Serial.println("auto light on");
      digitalWrite(lightPin, HIGH);
    }
    else
    {
      Serial.println("auto light off");
      digitalWrite(lightPin, LOW);
    }

    if (temp < tempSet)
    {
      Serial.println("auto temp on");
      digitalWrite(heatPin, HIGH);
    }
    else
    {
      Serial.println("auto temp off");
      digitalWrite(heatPin, LOW);
    }
  }
  else
  {
    if (lightOn)
    {
      Serial.println("light on");
      // led su esp32
      // digitalWrite(2, HIGH);
      digitalWrite(luxPin, HIGH);
    }
    else
    {
      Serial.println("light off");
      digitalWrite(luxPin, LOW);
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

  if (light <= (prevLight - LIGHT_RANGE) || light >= (prevLight + LIGHT_RANGE))
  {
    String stLight = String(topic_light) + "#" + light;
    client.publish(topic_light, stLight.c_str());
    prevLight = light;
  }

  if (temp <= (prevTemp - TEMP_RANGE) || temp >= (prevTemp + TEMP_RANGE))
  {
    String stTemp = String(topic_temp) + "#" + temp;
    client.publish(topic_temp, stTemp.c_str());
    prevTemp = temp;
  }

  delay(500);
}
