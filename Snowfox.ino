int channel[14] = {}; //defines channel[0] - channel[13]

void setup() {
  Serial.begin(115200);
    for (int i = 0; i <= 13; i++) //initialize all pins as INPUT'S
    {
       pinMode(i, INPUT);
    }
}

void loop() {
  for (int i = 0; i <= 13; i++) //reading in PWM'S on Pin's 0-13 and print them on Serial Port
  {
      channel[i] = pulseIn(i, HIGH);
      Serial.println(channel[i]);
  }
}
