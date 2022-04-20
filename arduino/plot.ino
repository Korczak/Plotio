#include <AccelStepper.h>

AccelStepper XAxis(1, 3, 6);
AccelStepper YAxis(1, 4, 7);
AccelStepper ZAxis(1, 11, 12);
int valueX;
int valueY;
int valueZ;
int speedXY = 500;
int speedZ = 500;
int alarmStatus;
int workStatus;
int Xdirection;
int Ydirection;
int Xposition;
int Yposition;
String cod;

void setup() {
  XAxis.setMaxSpeed(800);
  YAxis.setMaxSpeed(800);
  ZAxis.setMaxSpeed(800);
  //pinMode(9, INPUT_PULLUP);
  //pinMode(10, INPUT_PULLUP);
  Serial.begin(115200);
  Serial.setTimeout(10);
}

void loop() {
  if(Serial.available()) {
    cod = Serial.readString();
    if(cod.indexOf("POZYCJONOWANIE") >= 0) {
      Homing();
      SendResponse(alarmStatus, 1, XAxis.currentPosition(), YAxis.currentPosition());
    }
    if (cod.indexOf("RESET") >= 0) {
      Reset();
      SendResponse(alarmStatus, 1, XAxis.currentPosition(), YAxis.currentPosition());
    }
    else if (cod.indexOf("USTAWIENIA") >= 0) {
      toCharSpeed(cod);
    }
    else if (cod.indexOf("KOMENDA") >= 0) {
      toChar(cod);
      if (valueX <= 0 && valueY <= 0) {
        GoTo(valueX, valueY, valueZ);
      }
    }
    else if (cod.indexOf("TEST") >= 0) {
      test();
    }
  }
}

void test() {
  Serial.write("KOMENDA,0,0,1");
  Serial.write("KOMENDA,0,10,1");
  Serial.write("KOMENDA,0,15,1");
  Serial.write("KOMENDA,0,20,1");
  Serial.write("KOMENDA,0,25,1");
}

void Reset() {
  if (digitalRead(9) != 0) {
    if (Xdirection > 0) {
      Xposition = XAxis.currentPosition() - 60;
      while (XAxis.currentPosition() != Xposition) {
        XAxis.setSpeed(-speedXY);
        XAxis.runSpeed();
        SendResponse(alarmStatus, 0, XAxis.currentPosition(), YAxis.currentPosition());
      }
    }
    else {
      Xposition = XAxis.currentPosition() + 60;
      while (XAxis.currentPosition() != Xposition) {
        XAxis.setSpeed(speedXY);
        XAxis.runSpeed();
        SendResponse(alarmStatus, 0, XAxis.currentPosition(), YAxis.currentPosition());
      }
    }
  }
  if (digitalRead(10) != 0) {
    if (Ydirection > 0) {
      Yposition = YAxis.currentPosition() - 60;
      while (YAxis.currentPosition() != Yposition) {
        YAxis.setSpeed(-speedXY);
        YAxis.runSpeed();
        SendResponse(alarmStatus, 0, XAxis.currentPosition(), YAxis.currentPosition());
      }
    }
    else {
      Yposition = YAxis.currentPosition() + 60;
      while (YAxis.currentPosition() != Yposition) {
        YAxis.setSpeed(speedXY);
        YAxis.runSpeed();
        SendResponse(alarmStatus, 0, XAxis.currentPosition(), YAxis.currentPosition());
      }
    }
  }
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  SendResponse(alarmStatus, 1, XAxis.currentPosition(), YAxis.currentPosition());
}

void Homing() {
  while (digitalRead(9) == 0) {
    XAxis.setSpeed(speedXY);
    XAxis.runSpeed();
  }
  XAxis.setCurrentPosition(0);
  while (XAxis.currentPosition() != -60) {
    XAxis.setSpeed(-speedXY);
    XAxis.runSpeed();
  }
  XAxis.setCurrentPosition(0);
  while (digitalRead(10) == 0) {
    YAxis.setSpeed(speedXY);
    YAxis.runSpeed();
    }
  YAxis.setCurrentPosition(0);
  while (YAxis.currentPosition() != -60) {
    YAxis.setSpeed(-speedXY);
    YAxis.runSpeed();
  }
  YAxis.setCurrentPosition(0);
  SendResponse(alarmStatus, 1, XAxis.currentPosition(), YAxis.currentPosition());
}

void GoTo(int valueX, int valueY, int valueZ) { 
  if (digitalRead(9) == 0 && digitalRead(10) == 0) {
    alarmStatus = 0;
  }
  int responseNumber = 0;
  if (XAxis.currentPosition() > valueX) {
    XAxis.setSpeed(-speedXY);
    Xdirection = -1;
  }
  else if (XAxis.currentPosition() < valueX) {
    XAxis.setSpeed(speedXY);
    Xdirection = 1;
  }
  if (YAxis.currentPosition() > valueY) {
    YAxis.setSpeed(-speedXY);
    Ydirection = -1;
  }
  else if (YAxis.currentPosition() < valueY) {
    YAxis.setSpeed(500);
    Ydirection = 1;
  }
  while ((XAxis.currentPosition() != valueX || YAxis.currentPosition() != valueY) && alarmStatus == 0) {
    if (XAxis.currentPosition() != valueX) {
      XAxis.runSpeed();
    }
    if (YAxis.currentPosition() != valueY) {
      YAxis.runSpeed();
    }
    if (digitalRead(9) != 0) {
      alarmStatus = 1;
    }
    if (digitalRead(10) != 0) {
      alarmStatus = 2;
    }
    responseNumber = responseNumber + 1;
    if (responseNumber % 10000 == 0) {
      SendResponse(alarmStatus, 0, XAxis.currentPosition(), YAxis.currentPosition());
    }
    //Serial.println(responseNumber);
  }
  if (valueZ != 0 && alarmStatus == 0) {
    for (int licznik = 0; licznik < valueZ; licznik++){
      ZAxis.setSpeed(speedZ);
      while (ZAxis.currentPosition() != 1 && alarmStatus == 0) {
        ZAxis.runSpeed();
      }
      delay(100);
      ZAxis.setSpeed(-speedZ);
      while (ZAxis.currentPosition() != 0 && alarmStatus == 0) {
        ZAxis.runSpeed();
      }
    }
  }
  SendResponse(alarmStatus, 1, XAxis.currentPosition(), YAxis.currentPosition());
}

void SendResponse(int workStatus, int alarmStatus, int valueXResponse, int valueYResponse) {
  Serial.print(workStatus);
  Serial.print(",");
  Serial.print(alarmStatus);
  Serial.print(",");
  Serial.print(ConvertToPixels(valueXResponse));
  Serial.print(",");
  Serial.print(ConvertToPixels(valueYResponse));
  Serial.println(",|");
}

int ConvertToSteps(int value) {
  value = -3 * value;
  return value;
}

int ConvertToPixels(int value) {
  value = value/(-3);
  return value;
}

void toChar(String cod) {
  char *str = new char[cod.length() + 1];
  strcpy(str, cod.c_str());
  const size_t bufferSize = 4;
  int arr[bufferSize];
  char *p = strtok(str, ",");
  size_t index = 0;
  while (p != nullptr && index < bufferSize) {
    arr[index++] = atoi(p);
    p = strtok(NULL, ",");
  }
  valueX = ConvertToSteps(arr[1]);
  valueY = ConvertToSteps(arr[2]);
  valueZ = arr[3];
  delete [] str;
}

void toCharSpeed(String cod) {
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
  speedXY = arr[1];
  speedZ = arr[2];
  delete [] str;
}