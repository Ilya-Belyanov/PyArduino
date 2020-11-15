#include <Ultrasonic.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//SENSORS
#define SENSOR_LIGHT A0
#define SENSOR_LINE A1
#define SENSOR_TEMPERATURE 2
#define SENSOR_DISTANT_ECHO 12
#define SENSOR_DISTANT_TRG 13

//MODULES
#define LASER 3
#define LED_DISTANCE 4

//RGB LED
#define R 11
#define G 10
#define B 9

int colorR, colorG, colorB;
int distance_value;

Ultrasonic distant(SENSOR_DISTANT_ECHO, SENSOR_DISTANT_TRG);

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire temperature(SENSOR_TEMPERATURE);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature temp_sensors(&temperature);

//For reading command 
String command;
char chr;
  
void setup() 
{
  Serial.begin(115200);
  
  temp_sensors.begin();
  
  pinMode(LASER, OUTPUT);
  pinMode(LED_DISTANCE, OUTPUT);
  
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);

}

void loop() 
{
  if (Serial.available())
  { 
    checkCommand();

    //Read sensors
    if (command[0] == 'i')
      Serial.println(analogRead(SENSOR_LIGHT));
      
    else if (command[0] == 'l')
      Serial.println(analogRead(SENSOR_LINE));

    else if (command[0] == 'd')
    { distance_value = distant.read();
      distance_analysis(distance_value);
      Serial.println(distance_value);
    }
      
    else if (command[0] == 't')
    {
      temp_sensors.requestTemperatures();
      Serial.println(temp_sensors.getTempCByIndex(0)); 
    }

    else if (command[0] == 'z')
    {
      if (command[1] == '0')
        digitalWrite(LASER, LOW);
      else
        digitalWrite(LASER, HIGH);
    }
    else if (command[0] == 's')
        digitalWrite(LED_DISTANCE, LOW);
      
    else if (command[0] == 'r')
    { 
      colorR = command.substring(1, command.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }
    else if (command[0] == 'g')
    { 
      colorG = command.substring(1, command.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }
    else if (command[0] == 'b')
    { 
      colorB = command.substring(1, command.length() - 1).toInt();
      color(colorR, colorG, colorB); 
    }    

    else if (command[0] == 'E')
      reload();
  }
}

void checkCommand()
{
  delay(1);
    command = "";
    while (Serial.available())
    { 
      chr = Serial.read();
      command.concat(chr);
    }
}

void distance_analysis(int distance_value)
{
  if (distance_value > 10)
    digitalWrite(LED_DISTANCE, LOW);
  else
    digitalWrite(LED_DISTANCE, HIGH);
}

void color(unsigned char red, unsigned char green, unsigned char blue)
{
  analogWrite(R, red);
  analogWrite(G, green);
  analogWrite(B, blue);
  
}

void reload()
{
  color(0, 0, 0);
  digitalWrite(LED_DISTANCE, LOW);
  digitalWrite(LASER, LOW);
}
