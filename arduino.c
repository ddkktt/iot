#ifndef EDU_INO_0022
#define EDU_INO_0022

// Include libraries
#include <Arduino.h>

// Define analog input pins
const int smokeA0 = A0;  // Smoke sensor
const int buzzer = 8;    // Buzzer

// Define variables
float sensorValue;  // Variable to store sensor value

void setup() {
  pinMode(buzzer, OUTPUT);      // Set buzzer pin as output
  pinMode(smokeA0, INPUT);       // Set smoke sensor pin as input

  Serial.begin(9600);            // Initialize serial communication at 9600 baud
  Serial.println("Gas sensor warming up!");
  delay(2000);                     // Wait for 2 seconds
  noTone(buzzer);                  // Stop any sound on buzzer
}

void loop() {
  sensorValue = analogRead(smokeA0);  // Read analog value from smoke sensor
             sensorValue = analogRead(smokeA0); // read analog pin A0

             Serial.print("Sensor Value: ");
             Serial.print(sensorValue);

             if (sensorValue > 300)
             (

                                        Serial.print(" | Smoke detected!");
                                        tone (buzzer, 1000, 200);

             else (                     noTone (buzzer);

             }
             Serial.println("");

             delay(200); // wait 2s for next reading



}

#endif