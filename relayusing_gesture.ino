// Pin definitions for relay control
const int relay1 = 7;  // Relay 1 connected to pin 7
const int relay2 = 6;  // Relay 2 connected to pin 6
const int relay3 = 5;  // Relay 3 connected to pin 5
const int relay4 = 4;  // Relay 4 connected to pin 4

void setup() {
  // Set relay pins as output
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  
  // Initialize all relays to off (HIGH = OFF for active-low relays)
  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
  digitalWrite(relay3, HIGH);
  digitalWrite(relay4, HIGH);

  // Begin serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available from the serial port
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming byte
    
    // Control the relays based on the received command
    switch (command) {
      case '1':
        digitalWrite(relay1, LOW);  // Turn ON relay 1
        break;
      case '0':
        digitalWrite(relay1, HIGH); // Turn OFF relay 1
        break;
      case '2':
        digitalWrite(relay2, LOW);  // Turn ON relay 2
        break;
      case '3':
        digitalWrite(relay2, HIGH); // Turn OFF relay 2
        break;
      case '4':
        digitalWrite(relay3, LOW);  // Turn ON relay 3
        break;
      case '5':
        digitalWrite(relay3, HIGH); // Turn OFF relay 3
        break;
      case '6':
        digitalWrite(relay4, LOW);  // Turn ON relay 4
        break;
      case '7':
        digitalWrite(relay4, HIGH); // Turn OFF relay 4
        break;
    }
  }
}
