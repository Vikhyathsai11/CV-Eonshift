#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi configuration
const char* ssid = "V";
const char* password = "123456789";

// MQTT configuration
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "/image";

const int led_pin = D1;  // GPIO pin connected to the LED

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.begin(115200);
  Serial.println();

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  char message[length + 1];
  for (int i = 0; i < length; i++) {
    message[i] = (char)payload[i];
  }
  message[length] = '\0';
  
  Serial.println(message);

  // Parse the message to extract the value
  int value = atoi(message);

  if (strcmp(topic, mqtt_topic) == 0) {
    if (value == 1) {
      digitalWrite(led_pin, HIGH);  // Turn on the LED when "1" is received
    } else if (value == 0) {
      digitalWrite(led_pin, LOW);  // Turn off the LED when "0" is received
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("NodeMCU_Client")) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);  // Make sure LED is initially off

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
