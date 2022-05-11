//Program code for Arduino Uno to record sensor data and send via serial monitor
//Sensor data are randomly generated for demonstration

//Temperature and Humidity Variable Initialization
long loc1_temp; 
long loc2_temp;
long loc1_hum;
long loc2_hum;

unsigned long Time =2000; //120000 //(2 minutes)time interval data records

void setup() {
  Serial.begin(9600);
  
}
void loop() {

//Random sensor data generation, in real world analog signal from sensor can be read from analogRead() function
loc1_temp=random(64,72);
loc2_temp=random(68,73);
loc2_hum=random(56,63);
loc1_hum=random(55,60);

//serial monitor outputing in the format: latitude1 Longitude1 Temperature1 Humidity1 Latitude2 Longitude2 Temperature2 Humidity2
//example: 33.948 -83.377 80 50 31.479 -83.521 85 60
Serial.print("33.948 -83.377 ");  //Latitude and Longitude of a Location 1
Serial.print(loc1_temp);          // Temperature1 at Location 1
Serial.print(" ");
Serial.print(int(loc1_hum));      // Humidity1 at Location 1
Serial.print(" ");
Serial.print("31.479 -83.521 ");   // Latitude and Longitude of a Location 2
Serial.print(loc2_temp);          //Temperature1 at Location 2
Serial.print(" ");
Serial.println(int(loc2_hum));    //Humidity at Location 2
  
delay(Time); //Time interval between data records
}
