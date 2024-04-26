/*
 Name:		RFID.cpp
 Created:	26.04.2024 14:32:53
 Author:	apart
 Editor:	http://www.visualmicro.com
*/

#include "RFID.h"

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

const char* ssid = "Department of Physics";
const char* password = "beinlovewithphysics";
const char* host = "api.telegram.org";
const int httpsPort = 443;
const char* botToken = "YOUR_BOT_TOKEN";

WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  client.setInsecure(); // Необходимо для ESP8266 для подключения без проверки сертификата
}

void loop() {
  if (client.connect(host, httpsPort)) {
    String message = "Hello, Telegram!";
    String url = "/bot" + String(botToken) + "/sendMessage?chat_id=YOUR_CHAT_ID&text=" + message;
    
    client.println("GET " + url + " HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("Connection: close");
    client.println();

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        break;
      }
    }
    String line = client.readStringUntil('\n');
    Serial.println(line);
  } else {
    Serial.println("Connection failed");
  }

  delay(10000); // Отправка сообщения каждые 10 секунд
}
