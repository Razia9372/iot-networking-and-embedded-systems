#include <WiFi.h>
#include <esp_now.h>
#include <esp_sleep.h>

#define PIR_PIN 12
#define LDR_PIN 34
#define LED_PIN 2
#define SLEEP_TIME 1.3

uint8_t broadcastAddress[] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};
esp_now_peer_info_t peerInfo;

// just to check if the data was sent correctly
void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Send OK" : "Send Fail");
}

void setup() {
  Serial.begin(115200);
  delay(500);  // wait a bit so serial monitor is ready

  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  // WiFi is needed for ESP-NOW
  WiFi.mode(WIFI_STA);

  // initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW error");
    return;
  }

  // register callback to know if sending worked
  esp_now_register_send_cb(OnDataSent);

  // set receiver address (here broadcast)
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);
}

void loop() {

  Serial.println("---- CYCLE ----");

  // start measuring sensor reading time
  unsigned long t1 = micros();

  // read sensors
  int motion = digitalRead(PIR_PIN);   // motion: HIGH or LOW
  int light = analogRead(LDR_PIN);     // light level from LDR

  char msg[60];

  // create message depending on motion
  if (motion == HIGH) {
    sprintf(msg, "MOTION_DETECTED-LUMINOSITY:%d", light);
    Serial.println("Motion detected");
  } else {
    sprintf(msg, "MOTION_NOT_DETECTED-LUMINOSITY:%d", light);
    Serial.println("No motion");
  }

  // time spent reading sensors
  unsigned long readTime = micros() - t1;

  // start measuring transmission time
  unsigned long t2 = micros();

  Serial.print("Sending: ");
  Serial.println(msg);

  // send data using ESP-NOW
  esp_now_send(broadcastAddress, (uint8_t*)msg, strlen(msg));

  // time spent in sending function
  unsigned long txTime = micros() - t2;

  // start measuring processing (what we call idle here)
  unsigned long t3 = micros();

  // simple logic to turn LED on/off
  if (motion == HIGH && light > 2000) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("Light ON");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("Light OFF");
  }

  // this delay keeps the system active (this is actually wasting energy)
  delay(200);

  // time spent in this part
  unsigned long idleTime = micros() - t3;

  // print all measured times
  Serial.println("---- TIMES ----");

  Serial.print("Read: ");
  Serial.print(readTime);
  Serial.println(" us");

  Serial.print("TX: ");
  Serial.print(txTime);
  Serial.println(" us");

  Serial.print("Idle: ");
  Serial.print(idleTime);
  Serial.println(" us");

  Serial.print("Sleep: ");
  Serial.print(SLEEP_TIME);
  Serial.println(" s");

  Serial.println("----------------");

  Serial.flush();

  Serial.println("Sleep...");
  Serial.flush();

  // set timer for next wake-up
  esp_sleep_enable_timer_wakeup(SLEEP_TIME * 1000000);

  // go to deep sleep (everything stops here)
  esp_deep_sleep_start();
}