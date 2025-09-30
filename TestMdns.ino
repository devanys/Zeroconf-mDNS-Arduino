#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <ArduinoMDNS.h>

const char* ssid     = "";
const char* password = "";

IPAddress local_IP(192, 168, 1, 150);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

WiFiServer server(80);
int ledPin = 13;
bool ledState = false;

WiFiUDP udp;
MDNS mdns(udp);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  WiFi.config(local_IP, gateway, subnet);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi Connected");
  Serial.print("Arduino IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();

  if (!mdns.begin(WiFi.localIP(), "arduino")) {
    Serial.println("❌ mDNS failed!");
  } else {
    Serial.println("✅ mDNS responder started → http://arduino.local");
    mdns.addServiceRecord("arduino", 80, MDNSServiceTCP, "http");
  }
}

void loop() {
  mdns.run();  

  WiFiClient client = server.available();
  if (!client) return;

  while (client.connected() && !client.available()) delay(1);

  String request = client.readStringUntil('\n');
  request.toLowerCase();
  client.flush();

  String response = "";

  if (request.indexOf("/on") != -1) {
    digitalWrite(ledPin, HIGH);
    ledState = true;
    response = "ON";
  } else if (request.indexOf("/off") != -1) {
    digitalWrite(ledPin, LOW);
    ledState = false;
    response = "OFF";
  } else if (request.indexOf("/status") != -1) {
    response = ledState ? "STATUS: ON" : "STATUS: OFF";
  } else if (request.indexOf("/favicon.ico") != -1) {
    response = "OK";
  } else {
    response = "UNKNOWN CMD";
  }

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain");
  client.println("Connection: close");
  client.println();
  client.println(response);
  client.stop();
}
