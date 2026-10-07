#include <WiFi.h>
#include <esp_now.h>
#include <esp_sleep.h>

#define PIR_PIN 33
#define LDR_PIN 34
#define LED_PIN 2

uint8_t address[] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};
esp_now_peer_info_t peer;

// just to see if sending worked
void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Send OK" : "Send Fail");
}

void setup() {
  Serial.begin(115200);
  delay(300);   // give time for serial to start

  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("cycle start");

  // start measuring total active time
  unsigned long startTime = micros();

  // read sensors
  unsigned long readStart = micros();

  int motionValue = digitalRead(PIR_PIN);   // 1 if motion detected
  int lightValue = analogRead(LDR_PIN);     // light intensity

  unsigned long readDuration = micros() - readStart;

  // build message to send
  char message[60];

  if (motionValue == HIGH) {
    sprintf(message, "MOTION:%d", lightValue);
    Serial.println("motion detected");
  } else {
    sprintf(message, "NO_MOTION:%d", lightValue);
    Serial.println("no motion");
  }

  // turn on WiFi only when needed
  WiFi.mode(WIFI_STA);

  if (esp_now_init() == ESP_OK) {

    esp_now_register_send_cb(OnDataSent);

    memcpy(peer.peer_addr, address, 6);
    peer.channel = 0;
    peer.encrypt = false;
    esp_now_add_peer(&peer);

    // send the message and measure time
    unsigned long txStart = micros();

    Serial.print("sending: ");
    Serial.println(message);

    esp_now_send(address, (uint8_t*)message, strlen(message));

    unsigned long txDuration = micros() - txStart;

    // small wait so transmission completes
    delay(300);

    // simple logic for LED
    unsigned long processStart = micros();

    if (motionValue == HIGH && lightValue > 2000) {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("light on");
    } else {
      digitalWrite(LED_PIN, LOW);
      Serial.println("light off");
    }

    // this delay makes processing longer (not really needed)
    delay(200);

    unsigned long processDuration = micros() - processStart;

    // total time from wake to sleep
    unsigned long totalActiveTime = micros() - startTime;

    // print all times
    Serial.println("times:");

    Serial.print("read: ");
    Serial.print(readDuration);
    Serial.println(" us");

    Serial.print("tx: ");
    Serial.print(txDuration);
    Serial.println(" us");

    Serial.print("processing: ");
    Serial.print(processDuration);
    Serial.println(" us");

    Serial.print("total: ");
    Serial.print(totalActiveTime);
    Serial.println(" us");

    Serial.println();
  }

  // wait until motion goes away so it doesn't wake up again immediately
  while (digitalRead(PIR_PIN) == HIGH) {
    delay(10);
  }

  // wake up only when motion happens again
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);

  Serial.println("going to sleep...");
  Serial.flush();

  // enter deep sleep
  esp_deep_sleep_start();
}

void loop() {
}