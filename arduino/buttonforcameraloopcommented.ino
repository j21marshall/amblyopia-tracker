#include <SoftwareSerial.h> 
byte incomingbyte;
SoftwareSerial cameraSerial = SoftwareSerial(2, 3); //Sets pins 2 and 3 as RX and TX for the camera
int a=0x0000,  //Read Starting address     
    j=0,
    k=0,
    count=0;
uint8_t MH,ML;
boolean EndFlag=0;
const int  buttonPin = 9;    // the pin that the pushbutton is attached to
const int ledPin = 10;       // the pin that the LED is attached to

// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button

//Send Reset command
void SendResetCmd() {
  cameraSerial.write((byte)0x56);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x26);
  cameraSerial.write((byte)0x00);   
}

//Send take picture command
void SendTakePhotoCmd() {
  cameraSerial.write((byte)0x56);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x36);
  cameraSerial.write((byte)0x01);
  cameraSerial.write((byte)0x00);
    
  a = 0x0000; //reset so that another picture can taken
}
//Frame size of image
void FrameSize() {
  cameraSerial.write((byte)0x56);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x34);
  cameraSerial.write((byte)0x01);
  cameraSerial.write((byte)0x00);  
}

//Read data
void SendReadDataCmd() {
  MH=a/0x100;
  ML=a%0x100;
      
  cameraSerial.write((byte)0x56);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x32);
  cameraSerial.write((byte)0x0c);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x0a);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)MH);
  cameraSerial.write((byte)ML);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x20);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x0a);

  a+=0x20; 
}
//Stop image command
void StopTakePhotoCmd() {
  cameraSerial.write((byte)0x56);
  cameraSerial.write((byte)0x00);
  cameraSerial.write((byte)0x36);
  cameraSerial.write((byte)0x01);
  cameraSerial.write((byte)0x03);        
}

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(ledPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(38400); //Serial Port Data rate
  cameraSerial.begin(38400); //Camera data rate
  SendResetCmd();
  delay(1000);
}


void loop() {
  buttonState = digitalRead(buttonPin);//to set the state of the system according to pin 9

  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) { //when pin 9 is high pout put no pic
      Serial.println("No pic");
      digitalWrite(ledPin, HIGH);//LED ON
    } else {//when pin 9 is low take a certain number of pictures
      for(int i=0; i < 4; i++){
      SendTakePhotoCmd();
      digitalWrite(ledPin, LOW); //LED OFF
      Serial.print("Start");
  delay(100);
  while(cameraSerial.available()>0) {
    incomingbyte=cameraSerial.read();
  }
  byte b[32];
      
  while(!EndFlag) {  //code below to send data iof image from the camera to the MCU 
    j=0;
    k=0;
    count=0;
    SendReadDataCmd();
           
    delay(75); //try going up
    while(cameraSerial.available()>0) {
      incomingbyte=cameraSerial.read();
      k++;
      if((k>5)&&(j<32)&&(!EndFlag)) {
        b[j]=incomingbyte;
        if((b[j-1]==0xFF)&&(b[j]==0xD9))
        EndFlag=1;                           
        j++;
        count++;
      }
    }
            
    for(j=0;j<count;j++) {   
      if(b[j]<0x10)
        Serial.print("0");
      Serial.print(b[j], HEX);//send the data to the Serial Monitor
    }
    Serial.print("");//changed from serial.println();
  }
  
  delay(100);
  StopTakePhotoCmd(); //stop this picture so another one can be taken
  EndFlag = 0; //reset flag to allow another picture to be read
  //Serial.println();//added
  Serial.println("End");
  //Serial.println();
  delay(100);
    }
    }
  }
   
  lastButtonState = buttonState;
}
