 /*
 * Power Metering for REMROB-Plattform
 *
 * Reading from S0-impulse Interface(EN 62053-31) of Powermeter, and writing pulses into EEPROM.
 * Transfer data via Yun-Bridge  
 *
 * Author: Michael Macherey
 * 
 */
 
#include <EEPROMex.h>
#include <Bridge.h>

// ################ vars S0 Interface #############################

// constant used to identify EEPROM addresses

const int addressOnEEPROMone = 7;                     // the EEPROM address used to store the impulse of Powermeter "One"
const int addressOnEEPROMtwo = 14;                     // the EEPROM address used to store the impulse of Powermeter "Two"

// Writing and retrieving double = 1010102.500,this are four bytes of EEPROM memory.
double outputOfEEPROMone;
double outputOfEEPROMtwo;

// Interrupt at SZero(S0) Pin
const int SZeroPinOne = 2;                           // initializing S0 Pin
const int SZeroPinTwo = 3;                           // initializing S0 Pin

//################ end S0 Interface ####################################

void setup() {
  
  // needed only for debugging purpose at Serial Monitor
  Serial.begin(9600);
  
 
  // ################# setup S0 Interface ################################
  
  pinMode(SZeroPinOne, INPUT);                            // defining SZeroPinOne as INPUT/OUTPUT
  pinMode(SZeroPinTwo, INPUT);                            // defining SZeroPinOne as INPUT/OUTPUT
  
  attachInterrupt(1, saveImpulseToEEPROMone, FALLING);   // Interrupt settings for Arduino-Yun "int.1" the same as on Leonardo
  attachInterrupt(0, saveImpulseToEEPROMtwo, FALLING);   // Interrupt settings for Arduino-Yun "int.0" the same as on Leonardo
  
  // ################# setup bridge ##########################################
  
  pinMode(12,OUTPUT);          // defining pin 12 as OUTPUT for bridge communication
  
  // this is for debugging purpose with onboard LED
  // pinMode(13,OUTPUT);
  
  Bridge.begin();             // Starts Bridge, facilitating communication between the AVR and Linux processor
                              // begin() is a blocking function, this process takes approximately three seconds.
  // ################# end setup bridge ######################################
}

void loop() {
  
  // ######### begin bridge ##########
  
  Bridge.put("PowerMeterImpulseOne", String(0.001 + outputOfEEPROMone,3));  // Send Powermeter impulse with 3 decimals
  Bridge.put("PowerMeterImpulseTwo", String(0.001 + outputOfEEPROMtwo,3));  // Send Powermeter impulse with 3 decimals
  
  // ######### end bridge ##########
  
  // is for debugging purpose of S0 interface at Serial Monitor
  //delay(1000);
  debugTrace();

}

void readImpulseFromEEPROMone(){              // Read impulse from EEPROM "One"

  //Serial.println("inside ImpulseFromEEPROM" );
  outputOfEEPROMone = EEPROM.readDouble(addressOnEEPROMone);
}

void readImpulseFromEEPROMtwo(){              // Read impulse from EEPROM "Two"

  //Serial.println("inside ImpulseFromEEPROM" );
  outputOfEEPROMtwo = EEPROM.readDouble(addressOnEEPROMtwo);
}

void saveImpulseToEEPROMone(){                  // Save impulse to EEPROM 
  // Attention: The EEPROM has an endurance of at least 100,000 write/erase cycles.
    Serial.println("Interrupt");
   EEPROM.updateDouble(addressOnEEPROMone, 0.001 + outputOfEEPROMone);
   
}

void saveImpulseToEEPROMtwo(){                  // Save impulse to EEPROM 
  // Attention: The EEPROM has an endurance of at least 100,000 write/erase cycles.
    Serial.println("Interrupt");
   EEPROM.updateDouble(addressOnEEPROMtwo, 0.001 + outputOfEEPROMtwo);
   
}

void debugTrace(){
    // +++ the following block is for debugging purpose
   delay(500);
   if(digitalRead(SZeroPinOne)  == 1){
    /* 
    int dR = digitalRead(SZeroPinOne);
    Serial.print("dR = " );
    Serial.print(dR);
    */
    readImpulseFromEEPROMone();
    delay(50);
    Serial.print("EEPROMoneV= " );
    Serial.println(outputOfEEPROMone,3);
    Serial.print("");
    Serial.println("##################");
  }
  delay(500);
  if(digitalRead(SZeroPinTwo)  == 1){
    /* 
    int dR = digitalRead(SZeroPinTwo);
    Serial.print("dR = " );
    Serial.print(dR);
    */
    readImpulseFromEEPROMtwo();
    delay(50);
    Serial.print("EEPROMtwoV= " );
    Serial.println(outputOfEEPROMtwo,3);
    Serial.print("");
    Serial.println("##################");
  }
  
  // +++ end debugging block
}
