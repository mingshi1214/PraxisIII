// defines pins numbers
int stepPin = 3; int dirPin = 2;
void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT);
  pinMode(dirPin,OUTPUT);
  Serial.begin(9600);
}
void loop() {
  digitalWrite(dirPin,LOW); // Enables the motor to move in a particular direction
// Makes 200 pulses for making one full cycle rotation 
for(int x = 0; x < 200; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(2500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(2500); 
}
   /*digitalWrite(dirPin,LOW);
for(int x = 0; x < 200; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(900);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(900);*/
   Serial.print(stepPin);  
 // One second delay
}
