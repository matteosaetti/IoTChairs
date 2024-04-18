#include <WiFi.h>
#include <PubSubClient.h>

//TODO dal web devo riuscire ad accendere/spegnere le 2 luci,
//trovare un modo intelligente per gestire il rilascio della pressione
//per un tempo limitato lasciando accese le due luci 
// Definizione delle credenziali di rete
const char* ssid = "Nome della tua rete WiFi";
const char* password = "Password della tua rete WiFi";

// Indirizzo IP del Raspberry Pi che funge da broker MQTT
const char* mqtt_server = "192.168.18.10";

// Definizione del nome del client MQTT
const char* clientID = "ESP32Client";

// Definizione dei pin a cui sono collegati i sensori di temperatura e luce
const int temperatureSensorPin = A0; // Pin analogico per il sensore di temperatura
const int lightSensorPin = T1;       // Pin analogico per il sensore di luce
const int light1Pin = 5;             // Pin digitale per la prima luce
const int light2Pin = 4;             // Pin digitale per la seconda luce

// Soglie per temperatura e luce
const int temperatureThreshold = 25; // Soglia di temperatura (esempio)
const int lightThreshold = 500;      // Soglia di luce (esempio)

// Dichiarazione delle variabili globali
WiFiClient espClient;
PubSubClient client(espClient);

// Funzione per la connessione WiFi
void connectWiFi() {
  Serial.println("Connessione alla rete WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connessione in corso...");
  }
  Serial.println("Connessione WiFi stabilita");
}

// Funzione di callback MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  // Confronta il topic per determinare il tipo di messaggio ricevuto
  if (strcmp(topic, "pressure_status") == 0) {
    // Gestisce il messaggio relativo allo stato del sensore di pressione
    if (payload[0] == 'p') {
      // Se il sensore di pressione è premuto, controlla temperatura e luce
      int temperatureValue = analogRead(temperatureSensorPin);
      int lightValue = analogRead(lightSensorPin);

      // Controlla se temperatura e luce sono sotto le soglie
      if (temperatureValue < temperatureThreshold && lightValue < lightThreshold) {
        // Accendi le luci
        digitalWrite(light1Pin, HIGH);
        digitalWrite(light2Pin, HIGH);
      }
    } else {
      // Se il sensore di pressione non è premuto, spegni le luci
      digitalWrite(light1Pin, LOW);
      digitalWrite(light2Pin, LOW);
    }
  }
}

// Funzione per la connessione al server MQTT
void connectMQTT() {
  // Assegna la funzione di callback
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

  // Inizializza i pin per le luci come output
  pinMode(light1Pin, OUTPUT);
  pinMode(light2Pin, OUTPUT);

  // Connessione alla rete WiFi
  connectWiFi();

  // Connessione al server MQTT
  client.setServer(mqtt_server, 1883);
  connectMQTT();
}

void loop() {
  // Controllo della connessione al server MQTT
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();
}
