#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <PZEM004Tv30.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID"; // Thay bằng tên wifi 
const char* password = "YOUR_WIFI_PASSWORD"; // Thay bằng mật khẩu WiFi

// Django server URL
const char* serverUrl = "http://127.0.0.1:8000/api/sensor-data/";

// PZEM-004T pins
#define PZEM_RX_PIN D1 //Thay D1 bằng chân RX thực tế
#define PZEM_TX_PIN D2 //Thay D2 bằng chân TX thực tế
PZEM004Tv30 pzem(Serial, PZEM_RX_PIN, PZEM_TX_PIN);

// DHT11 configuration
#define DHTPIN D5 // Chân kết nối với cảm biến DHT11
#define DHTTYPE DHT11 // Loại cảm biến (Thay DHT11 bằng loại cảm biến nhiệt độ độ ẩm đang dùng)
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);

  // Khởi tạo cảm biến DHT11
  dht.begin();

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Read data from PZEM-004T
  float voltage = pzem.voltage();
  float current = pzem.current();
  float power = pzem.power();

  if (isnan(voltage) || isnan(current) || isnan(power)) {
    Serial.println("Error reading PZEM data");
    delay(2000);
    return;
  }

  // Read temperature and humidity from DHT11
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Error reading DHT11 data");
    delay(2000);
    return;
  }

  // Send data to Django server
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Create JSON payload
    String payload = "{\"voltage\":" + String(voltage) + 
                     ",\"current\":" + String(current) + 
                     ",\"power\":" + String(power) + 
                     ",\"temperature\":" + String(temperature) + 
                     ",\"humidity\":" + String(humidity) + "}";

    int httpCode = http.POST(payload);
    if (httpCode == HTTP_CODE_CREATED) {
      Serial.println("Data sent successfully");
    } else {
      Serial.println("Error sending data: " + String(httpCode));
    }
    http.end();
  }

  delay(300000); // Send data every 5 minutes
}