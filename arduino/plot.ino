#include <AccelStepper.h>
String cod;
int valueX;
int valueY;
int valueZ;
int Xposition;
int Yposition;
int Xdirection;
int Ydirection;
int alarmStatus;
int valueXResponse;
int valueYResponse;
int alarmStatusResponse;
AccelStepper XAxis(1, 3, 6);
AccelStepper YAxis(1, 4, 7);
AccelStepper ZAxis(1, 11, 12);

void setup() {
  Serial.begin(9600);
  XAxis.setMaxSpeed(400);
  YAxis.setMaxSpeed(400);
  ZAxis.setMaxSpeed(400);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
}

void loop() {
  while(Serial.available()) {
    cod = Serial.readString();
    delay(1000);
    if(cod.indexOf("home") >= 0) {
      Home();
    }
    else if(cod.indexOf("reset") >= 0) {
      Reset();
    }
    else {
      toChar(cod);
      if (valueX >= 0 && valueY >= 0 && (valueZ == 0) || (valueZ == 1)) {
        GoTo(valueX, valueY, valueZ);
      }
    }
    Serial.print(alarmStatus);
    Serial.print(",");
    Serial.print(valueXResponse);
    Serial.print(",");
    Serial.println(valueYResponse);
  }
}

void Home() {
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  while (alarmStatus == 0) {
    XAxis.setSpeed(300);
    XAxis.runSpeed();
    if (digitalRead(9) != 0) {
      alarmStatus = 1;
    }
  }
  XAxis.setCurrentPosition(0);
  while (XAxis.currentPosition() != -15) {
    XAxis.setSpeed(-300);
    XAxis.runSpeed();
  }
  XAxis.setCurrentPosition(0);
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  while (alarmStatus == 0) {
    YAxis.setSpeed(300);
    YAxis.runSpeed();
    if (digitalRead(10) != 0) {
      alarmStatus = 1;
    }
  }
  YAxis.setCurrentPosition(0);
  while (YAxis.currentPosition() != -15) {
    YAxis.setSpeed(-300);
    YAxis.runSpeed();
  }
  YAxis.setCurrentPosition(0);
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  valueXResponse = ConvertToPixels(XAxis.currentPosition());
  valueYResponse = ConvertToPixels(YAxis.currentPosition());
  alarmStatusResponse = alarmStatus;
}

void Reset() {
  if (digitalRead(9) != 0) {
    if (Xdirection == 0) {
      Xposition = XAxis.currentPosition() + 15;
      while (XAxis.currentPosition() != Xposition) {
        XAxis.setSpeed(400);
        XAxis.runSpeed();
      }
    }
    else {
      Xposition = XAxis.currentPosition() - 15;
      while (XAxis.currentPosition() != Xposition) {
        XAxis.setSpeed(-400);
        XAxis.runSpeed();
      }
    }
  }
  if (digitalRead(10) != 0) {
    if (Ydirection == 0) {
      Yposition = YAxis.currentPosition() + 15;
      while (YAxis.currentPosition() != Yposition) {
        YAxis.setSpeed(400);
        YAxis.runSpeed();
      }
    }
    else {
      Yposition = YAxis.currentPosition() - 15;
      while (YAxis.currentPosition() != Yposition) {
        YAxis.setSpeed(-400);
        YAxis.runSpeed();
      }
    }
  }
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  valueXResponse = ConvertToPixels(XAxis.currentPosition());
  valueYResponse = ConvertToPixels(YAxis.currentPosition());
  alarmStatusResponse = alarmStatus;
}

void GoTo(int valueX, int valueY, int valueZ) {
  valueX = ConvertToSteps(valueX);
  valueY = ConvertToSteps(valueY);
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  while ((XAxis.currentPosition() != valueX || YAxis.currentPosition() != valueY) && alarmStatus == 0) {
    if (abs(XAxis.currentPosition()) < -valueX) {
      XAxis.setSpeed(-400);
      XAxis.runSpeed();
      Xdirection = 0;
    }
    else if (abs(XAxis.currentPosition()) > -valueX) {
      XAxis.setSpeed(400);
      XAxis.runSpeed();
      Xdirection = 1;
    }
    if (abs(YAxis.currentPosition()) < -valueY) {
      YAxis.setSpeed(-400);
      YAxis.runSpeed();
      Ydirection = 0;
    }
    else if (abs(YAxis.currentPosition()) > -valueY) {
      YAxis.setSpeed(400);
      YAxis.runSpeed();
      Ydirection = 1;
    }
    if (digitalRead(9) != 0 || digitalRead(10) != 0) {
      alarmStatus = 1;
    }
  }
  if (valueZ == 1 && alarmStatus == 0) {
    ZAxis.move(1);
    ZAxis.runToPosition();
    delay(500);
    ZAxis.move(-1);
    ZAxis.runToPosition();
  }
  valueXResponse = ConvertToPixels(XAxis.currentPosition());
  valueYResponse = ConvertToPixels(YAxis.currentPosition());
  alarmStatusResponse = alarmStatus;
}

void toChar(String cod) {
  char *str = new char[cod.length() + 1];
  strcpy(str, cod.c_str());
  const size_t bufferSize = 3;
  int arr[bufferSize];
  char *p = strtok(str, ",");
  size_t index = 0;
  while (p != nullptr && index < bufferSize) {
    arr[index++] = atoi(p);
    p = strtok(NULL, ",");
  }
  valueX = arr[0];
  valueY = arr[1];
  valueZ = arr[2];
}

int ConvertToSteps(int value) {
  value = -3 * value;
  return value;
}

int ConvertToPixels(int value) {
  value = value/(-3);
  return value;
}
