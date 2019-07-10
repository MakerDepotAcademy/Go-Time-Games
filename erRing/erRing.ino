int ledPin = 17;      // on board LED PIN 17
int testLedPin = 16;	// on board LED PIN 16
int togglePin = 15;   // Toggle PIN

int triggerLedPin = 5;  // LED connected to digital pin 5
int IRSensorPin = 2;    // pushbutton connected to digital pin 7

int val = 0;                // variable to store the read value
bool buttonState = 0;       // variable to hold the button state
bool Mode = 0;              // What mode is the light in?

void setup() {
  pinMode(ledPin, OUTPUT);          // sets the digital pin ledPin as output
  pinMode(triggerLedPin, OUTPUT);   // sets the digital pin triggerLedPin as output
  pinMode(testLedPin, OUTPUT);      // sets the digital pin testLedPin as output

  pinMode(IRSensorPin, INPUT);      // sets the digital pin IRSensorPin as input
  pinMode(togglePin, INPUT_PULLUP); // sets the digital pin togglePin as input
}

void loop() {
	if (!digitalRead(togglePin)) {
  	if (!buttonState) {
      buttonState = true;
      Mode = !Mode; // this inverts button mode: If Mode was True - it will make it False and viseversa
  	}
  } else {
    buttonState = false;
  }

  if ( Mode  ) {
      val = digitalRead(IRSensorPin);     // read the IR sensor input pin
      digitalWrite(ledPin, !val);         // IR Senor on-board LED
      digitalWrite(triggerLedPin, val);   // IR Senor LED
  }

  digitalWrite(testLedPin, Mode);
}