// Definir pines
int smokeA0 = A0;
int ledPin = 11; // LED para indicar la detección de humo

void setup() {
  // Configurar pines
  pinMode(ledPin, OUTPUT);
  pinMode(smokeA0, INPUT);
  Serial.begin(9600); // Iniciar comunicación serial
  Serial.println("Sensor de humo calentando...");
  delay(20000); // Permitir que el sensor de humo se caliente
}

void loop() {
  // Leer valor del sensor
  int sensorValue = analogRead(smokeA0);

  // Comprobar si se detecta humo
  if (sensorValue > 300) {
    Serial.println("¡Humo o gas detectado!");
    // Encender LED indicador de humo
    digitalWrite(ledPin, HIGH);
  } else {
    Serial.println("Humo o gas no detectado");
    // Apagar LED indicador de humo
    digitalWrite(ledPin, LOW);
  }

  // Esperar un tiempo antes de tomar la siguiente lectura
  delay(2000);
}
