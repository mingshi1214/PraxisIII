//Motor 1
int enA = 9; 
int in1 = 8; 
int in2 = 5;
//65114 ticks
int ENSB1 = 4;
int ENSA1 = 3;

//Motor 2
int enB = 10; 
int in3 = 6; 
int in4 = 7;
//65128 ticks 
int ENSB2 = 12;
int ENSA2 = 2;

volatile unsigned int Count1 = 0;
volatile unsigned int Count2 = 0;

float drive_distance = 50;

float wheel_c = 3.14*6.5;

long int counts_per_rev_l = 520;
long int counts_per_rev_r = 524;

int target_count1 = 0;
int target_count2 = 0;

int motor_offset = 5;


int motor_power = 200;

void setup() {
  
  Serial.begin(9600);
  // set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(ENSB1, INPUT);
  pinMode(ENSA1, INPUT);
  
  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  pinMode(ENSB2, INPUT);
  pinMode(ENSA2, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENSA1), EncoderEvent1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENSA2), EncoderEvent2, CHANGE);

  delay(1000);
  //Serial.print("hello");
  driveStraight(drive_distance, motor_power);


}

void loop() { 
  
}


void driveStraight(float dist, int power){

    unsigned long num_ticks_l;
    unsigned long num_ticks_r;

    // Set initial motor power
    int power_l = 200;
    int power_r = 200;

  // Used to determine which way to turn to adjust
  unsigned long diff_l;
  unsigned long diff_r;

  // Reset encoder counts
  Count1 = 0;
  Count2 = 0;

  // Remember previous encoder counts
  unsigned long enc_l_prev = Count1;
  unsigned long enc_r_prev = Count2;

  // Calculate target number of ticks
  float num_rev = (dist) / wheel_c;  // Convert to mm
  unsigned long target_count1 = num_rev * counts_per_rev_l;
  unsigned long target_count2 = num_rev * counts_per_rev_r;
  Serial.println(target_count1);
  Serial.println(dist);
  Serial.println(counts_per_rev_l);
  Serial.println(num_rev);
  // Debug
  Serial.print("Driving for ");
  Serial.print(dist);
  Serial.print(" cm (");
  Serial.print(" ticks) at ");
  Serial.print(power);
  Serial.println(" motor power");
  Serial.println(Count1);
  Serial.println(target_count1);
  // Drive until one of the encoders reaches desired count
  while ( (Count1 < target_count1) && (Count2 < target_count2) ) {
    Serial.print("hello");
    // Sample number of encoder ticks
    num_ticks_l = Count1;
    num_ticks_r = Count2;

    // Print out current number of ticks
    Serial.print(num_ticks_l);
    Serial.print("\t");
    Serial.println(num_ticks_r);

    // Drive
    drive(power_l, power_r);

    // Number of ticks counted since last time
    diff_l = num_ticks_l - enc_l_prev;
    diff_r = num_ticks_r - enc_r_prev;

    // Store current tick counter for next time
    enc_l_prev = num_ticks_l;
    enc_r_prev = num_ticks_r;

    // If left is faster, slow it down and speed up right
    if ( diff_l > diff_r ) {
      power_l -= motor_offset;
      power_r += motor_offset;
    }

    // If right is faster, slow it down and speed up left
    if ( diff_l < diff_r ) {
      power_l += motor_offset;
      power_r -= motor_offset;
    }

    // Brief pause to let motors respond
    delay(20);
  }

  // Brake
  brake();
}


void drive(int power_a, int power_b) {

  // Constrain power to between -255 and 255
  power_a = constrain(power_a, -255, 255);
  power_b = constrain(power_b, -255, 255);

  // Left motor direction
  if ( power_a < 0 ) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }

  // Right motor direction
  if ( power_b < 0 ) {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } else {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }

  // Set speed
  analogWrite(enA, abs(power_a));
  analogWrite(enB, abs(power_b));
}
void brake() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}
// encoder event for the interrupt call
void EncoderEvent1() {
  Count1++;
}

void EncoderEvent2() {
  Count2++;
}
