#include <Ultrasonic.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define SENSOR_LINE A1
#define ONE_WIRE_BUS 2
#define R 11
#define G 10
#define B 9

String inChar;
char cha;

int colorR, colorG, colorB;

Ultrasonic ultrasonic(12, 13);

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup() 
{
  
  Serial.begin(115200);
  sensors.begin();
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);

}

void loop() 
{
  if (Serial.available())
  { 
    delay(1);
    inChar = "";
    while (Serial.available())
    { 
      cha = Serial.read();
      inChar.concat(cha);
    }

    if (inChar[0] == 'd')
      Serial.println(ultrasonic.read());    
    else if (inChar[0] == 'l')
      Serial.println(analogRead(SENSOR_LINE)); 
    else if (inChar[0] == 't')
    {
      sensors.requestTemperatures();
      Serial.println(sensors.getTempCByIndex(0)); 
    }
    else if (inChar[0] == 'r')
    { 
      colorR = inChar.substring(1, inChar.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }
    else if (inChar[0] == 'g')
    { 
      colorG = inChar.substring(1, inChar.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }
    else if (inChar[0] == 'b')
    { 
      colorB = inChar.substring(1, inChar.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }   

        
  }
}

void color(unsigned char red, unsigned char green, unsigned char blue)
{
  analogWrite(R, red);
  analogWrite(G, green);
  analogWrite(B, blue);
  
}
