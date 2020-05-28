
#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <SPI.h>

char msg[10];
RF24 radio(7,8);
const uint64_t pipe = 0x0a0c0a0c0aLL;
int lastmsg = 1;
String theMessage = "";
void setup(void){
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1,pipe);
  radio.startListening();
}
void loop(void){
  if (radio.available()){
    bool done = false;  
      done = radio.read(msg, 1); 
      char theChar = msg[0];
      if (msg[0] != 2){
        theMessage.concat(theChar);
        }
      else {
       Serial.println(theMessage);
       theMessage= ""; 
      }
   }
}
