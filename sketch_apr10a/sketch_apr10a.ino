#include <WiFi.h>
#include <PubSubClient.h>

// Definizione delle credenziali di rete
const char* ssid = "TIM-20606483";
const char* password = "Saio.1210!";

// Indirizzo IP del Raspberry Pi che funge da broker MQTT
const char* mqtt_server = "192.168.18.10";

// Definizione del nome del client MQTT
const char* clientID = "ESP32Client";

// Definizione del pin a cui è collegato il sensore di pressione
const int pressureSensorPin = A0; //Utilizziamo il pin A0 

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
  // Gestire il messaggio MQTT ricevuto
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
      // Iscrizione ai topic di interesse, se necessario
    } else {
      Serial.print("Errore, stato di connessione: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

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

  // Lettura del valore del sensore di pressione
  int pressureValue = analogRead(pressureSensorPin);

// Controllo se il sensore di pressione è attivato (es. sopra una certa soglia)
  if (pressureValue > 500) {
    // Invio del segnale MQTT solo se il sensore è attivato
    client.publish("pressure_status", "pressed");
  } else {
    // Invio del segnale MQTT di rilascio se il sensore non è attivato
    client.publish("pressure_status", "released");
  }
  delay(1000); // Puoi regolare la frequenza di invio dei dati
}