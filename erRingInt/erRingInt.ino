/*
  erRingInt

  Tests the escape room ring ATtiny45 microcontroller, LEDs and IR sensor.

  This program will test the escape room ring created by Maker Depot.
  The ring consists of an ATtiny45 microcontroller, a ring of LEDs and an IR sensor.

  When the user presses the button, the signal pin for the ATtiny45 will be set
  HIGH indicating to turn on the LEDs and IR sensor.  An interrupt will indicate that
  something has broken the IR beam and thus turn off the beam LEDs (The on board and
  the separate LED). If the button is not pressed, the ATtin45 pin will be set LOW
  and the ring will be in OFF mode (no LEDs and the IR sensor).

  modified 12 July 2019
  by Frank Cornacchiulo
*/

const byte signalPin = 14;       // The ATtiny45 signal pin
const byte onOffButtonPin = 15;  // ATtiny45 On/Off PIN
const byte testOnOffLedPin = 16; // ATtiny45

const byte interruptPin = 2;  // IR Sensor triggered pin
const byte ledPin = 17;       // IR Sensor triggered LED
const byte triggerLedPin = 5; // LED to indicate IR Sensor was triggered

bool onOffState = true;  // variable to hold the ATtinty On/Off state
bool buttonState = true; // variable to hold the button state

volatile byte state = LOW; // Initialize the IR sensor triggered state to LOW

void setup() {
  pinMode(signalPin, OUTPUT);       // Set the ATtiny45 signal pin
  pinMode(onOffButtonPin, INPUT);   // Set the digital pin for the ATTiny45 On/Off input
  pinMode(testOnOffLedPin, OUTPUT); // Set the digital pin testOnOffLedPin (indicates the ATTiny45 power is set on/off) as output

  pinMode(ledPin, OUTPUT);             // Set the IR Sensor triggered onboard LED pin to output
  pinMode(triggerLedPin, OUTPUT);      // Set the IR Sensor triggered LED pin to output
  pinMode(interruptPin, INPUT_PULLUP); // IR Sensor triggered pin to input

  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE); // create the interupt for the seneor trigger

  digitalWrite(signalPin, HIGH);
  digitalWrite(testOnOffLedPin, HIGH);
  digitalWrite(ledPin, LOW);
  digitalWrite(triggerLedPin, LOW);
}

void loop() {
  buttonState = digitalRead(onOffButtonPin);
  if (buttonState == LOW) {
    digitalWrite(signalPin, HIGH);
    digitalWrite(testOnOffLedPin, HIGH);
    onOffState = true;
  } else {
    digitalWrite(signalPin, LOW);
    digitalWrite(testOnOffLedPin, LOW);
    onOffState = false;
    state = LOW;
  }

  if (onOffState) {
    digitalWrite(ledPin, !state);
    digitalWrite(triggerLedPin, state);
  }
}

void blink() {
  state = !state;
}