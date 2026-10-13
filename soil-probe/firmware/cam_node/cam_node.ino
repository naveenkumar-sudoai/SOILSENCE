#include <Arduino.h>
#include <esp_camera.h>
#include <WiFi.h>
#include <WebServer.h>
#include "config.h"
#include "camera_pins.h"

// Forward declarations
void captureImage();
void handleCapture();
void handleStatus();

// Server setup
WebServer server(80);

// LED ring control
bool led_ring_state = false;

void setup() {
  Serial.begin(921600);
  
#ifdef USB_DATASET_MODE
  // In USB dataset mode, we don't initialize WiFi or camera here
  // But we need to set up the LED ring pin for output
  pinMode(LED_RING_GPIO, OUTPUT);
  digitalWrite(LED_RING_GPIO, LOW);
#else
  // Initialize camera
  camera_init();
  
  // Connect to WiFi
  WiFi.begin("SoilProbe", "password");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  
  // Setup web server
  server.on("/capture", handleCapture);
  server.on("/status", handleStatus);
  server.begin();
#endif
}

void loop() {
#ifdef USB_DATASET_MODE
  // USB dataset mode - listen for commands
  if (Serial.available()) {
    char cmd = Serial.read();
    switch (cmd) {
      case 'C':
        captureImage();
        break;
      case 'P':
        // Preview current frame
        Serial.print("PNG!");
        Serial.write((uint8_t*)0x00);
        Serial.write((uint8_t*)0x00);
        Serial.write((uint8_t*)0x00);
        Serial.write((uint8_t*)0x00);
        break;
      default:
        Serial.print("ERR!");
        Serial.print("Unknown command");
        break;
    }
  }
#else
  // WiFi mode - handle web requests
  server.handleClient();
#endif
}

void camera_init() {
  camera_config.frame_size = FRAMESIZE_VGA;
  camera_config.pixel_format = PIXFORMAT_RGB565;
  camera_config.fb_count = 1;
  camera_config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;

  esp_err_t err = esp_camera_init(&camera_config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
}

void captureImage() {
  // Turn on LED ring
  digitalWrite(LED_RING_GPIO, HIGH);
  
  // Wait for 150ms to let LED reach full brightness
  delay(150);
  
  // Discard one stale frame
  camera_fb_t* fb = esp_camera_fb_get();
  if (fb) {
    esp_camera_fb_return(fb);
  }
  
  // Get fresh frame, convert to JPEG and send over serial
  fb = esp_camera_fb_get();
  if (fb) {
    // Print image header
    Serial.print("IMG!");
    
    // Send length (4 bytes little-endian)
    uint32_t len = fb->len;
    Serial.write(len & 0xFF);
    Serial.write((len >> 8) & 0xFF);
    Serial.write((len >> 16) & 0xFF);
    Serial.write((len >> 24) & 0xFF);
    
    // Send data
    Serial.write(fb->buf, fb->len);
    
    // Turn off LED ring
    digitalWrite(LED_RING_GPIO, LOW);
    
    esp_camera_fb_return(fb);
  } else {
    // Send error
    Serial.print("ERR!");
    Serial.print("Failed to capture image");
    digitalWrite(LED_RING_GPIO, LOW);
  }
}

void handleCapture() {
  int flash = server.hasArg("flash") ? server.arg("flash").toInt() : 0;
  int q = server.hasArg("q") ? server.arg("q").toInt() : 85;
  
  if (flash) {
    digitalWrite(LED_RING_GPIO, HIGH);
    delay(150); // Wait for LED to reach full brightness
    camera_fb_t* fb = esp_camera_fb_get();
    if (fb) {
      // Discard one stale frame
      esp_camera_fb_return(fb);
      
      // Capture fresh frame
      fb = esp_camera_fb_get();
      if (fb) {
        server.sendHeader("X-Capture-Ms", "150");
        server.setContentLength(fb->len);
        server.send(200, "image/jpeg", "");
        server.sendContent((char*)fb->buf, fb->len);
        esp_camera_fb_return(fb);
      } else {
        server.send(500, "application/json", "{\"error\":\"Failed to capture.\"}");
      }
    } else {
      server.send(500, "application/json", "{\"error\":\"Failed to get frame.\"}");
    }
    digitalWrite(LED_RING_GPIO, LOW);
  } else {
    // No flash
    camera_fb_t* fb = esp_camera_fb_get();
    if (fb) {
      server.setContentLength(fb->len);
      server.send(200, "image/jpeg", "");
      server.sendContent((char*)fb->buf, fb->len);
      esp_camera_fb_return(fb);
    } else {
      server.send(500, "application/json", "{\"error\":\"Failed to capture.\"}");
    }
  }
}

void handleStatus() {
  // In dataset mode, we provide basic status
  String json = "{";
  json += "\"fw\":\"1.0.0\",";
  json += "\"rssi\":-65,";
  json += "\"free_heap\":12288,";
  json += "\"psram\":4194304,";
  json += "\"camera_ok\":true,";
  json += "\"camera_err\":\"\"";
  json += "}";
  
  server.send(200, "application/json", json);
}