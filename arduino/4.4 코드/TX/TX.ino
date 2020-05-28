#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <SPI.h>

char msg[10];
RF24 radio(7,8);
const uint64_t pipe = 0x0a0c0a0c0aLL;


void setup(void){
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipe);
}
void loop(void){
  String theMessage = "LEE DONG YEON";
  int messageSize = theMessage.length();
  for(int i=0 ; i< messageSize ; i++) {
    int charToSend[1];
    charToSend[0] = theMessage.charAt(i);
    radio.write(charToSend,1);
  }
  msg[0] =2;
  radio.write(msg,1);
  radio.powerDown();
  //delay(100);
  radio.powerUp();
  delay(1000);
}
