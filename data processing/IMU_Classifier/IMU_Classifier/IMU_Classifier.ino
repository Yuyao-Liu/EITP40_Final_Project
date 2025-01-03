#include <Arduino_LSM9DS1.h> // IMU Sensor Library for Arduino Nano 33 BLE Rev.1

#include <ArduTFLite.h>

#include "model.h"

const float accelerationThreshold = 2.5; // Threshold (in G values) to detect a "gesture" start
const int numSamples = 119; // Number of samples for a single gesture

int samplesRead; // sample counter 
const int inputLength = 714; // dimension of input tensor (6 values * 119 samples)

constexpr int tensorArenaSize = 8 * 1024;
alignas(16) byte tensorArena[tensorArenaSize];

// a simple table to map gesture labels
const char* GESTURES[] = {
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9"
};

#define NUM_GESTURES (sizeof(GESTURES) / sizeof(GESTURES[0]))

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // init IMU sensor
  if (!IMU.begin()) {
    Serial.println("IMU sensor init failed!");
    while (true); // stop program here.
  }

  // print IMU sampling frequencies
  Serial.print("Accelerometer sampling frequency = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sampling frequency = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");

  Serial.println();
  
  Serial.println("Init model..");
  if (!modelInit(model, tensorArena, tensorArenaSize)){
    Serial.println("Model initialization failed!");
    while(true);
  }
  Serial.println("Model initialization done.");
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;

  // wait for a significant movement
  while (true) {
    if (IMU.accelerationAvailable()) {
      // read linear acceleration
      IMU.readAcceleration(aX, aY, aZ);

      // compute absolute value of total acceleration
      float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

      // if total absolute acceleration is over the threshold a gesture has started
      if (aSum >= accelerationThreshold) {
        samplesRead = 0; // init samples counter
        break; // exit from waiting cycle
      }
    }
  }

  // reading cycle of all samples for current gesture
  while (samplesRead < numSamples) {
    // check if a sample is available
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      // read acceleration and gyroscope values
      IMU.readAcceleration(aX, aY, aZ);
      IMU.readGyroscope(gX, gY, gZ);

      // normalize sensor data because model was trained using normalized data
      aX = (aX + 4.0) / 8.0;
      aY = (aY + 4.0) / 8.0;
      aZ = (aZ + 4.0) / 8.0;
      gX = (gX + 2000.0) / 4000.0;
      gY = (gY + 2000.0) / 4000.0;
      gZ = (gZ + 2000.0) / 4000.0;
      
      // put the 6 values of current sample in the proper position
      // in the input tensor of the model
      modelSetInput(aX,samplesRead * 6 + 0);
      modelSetInput(aY,samplesRead * 6 + 1);
      modelSetInput(aZ,samplesRead * 6 + 2); 
      modelSetInput(gX,samplesRead * 6 + 3);
      modelSetInput(gY,samplesRead * 6 + 4);
      modelSetInput(gZ,samplesRead * 6 + 5); 
      
      samplesRead++;
      
      // if all samples are got, run inference
      if (samplesRead == numSamples) {
        if(!modelRunInference()){
          Serial.println("RunInference Failed!");
          return;
        }

        // get output values and print as percentage
        for (int i = 0; i < NUM_GESTURES; i++) {
          Serial.print(GESTURES[i]);
          Serial.print(": ");
          Serial.print(modelGetOutput(i)*100, 2);
          Serial.println("%");
        }
        Serial.println();
      }
    }
  }
}
