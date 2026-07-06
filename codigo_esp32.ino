// ================================
// Proyecto IoT - Cinta Transportadora ESP32
// Estudiante: Benjamin Pozo
// 2 sensores + 3 LEDs + buzzer
// ================================

// Sensores
const int SENSOR_ENTRADA = 18;
const int SENSOR_SALIDA  = 19;

// LEDs
const int LED_VERDE    = 23;
const int LED_AMARILLO = 22;
const int LED_ROJO     = 21;

// Buzzer
const int BUZZER = 25;

// Si tus sensores dan LOW cuando detectan, déjalo en LOW.
// Si dan HIGH cuando detectan, cambia LOW por HIGH.
const int SENSOR_ACTIVO = LOW;

// LEDs conectados desde GPIO -> resistencia -> LED -> GND
const int LED_ON  = HIGH;
const int LED_OFF = LOW;

// Variables de estado
bool alarma = false;
bool contandoSalida = false;

unsigned long tiempoInicioSalida = 0;
const unsigned long TIEMPO_ALARMA = 5000; // 5 segundos

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(SENSOR_ENTRADA, INPUT);
  pinMode(SENSOR_SALIDA, INPUT);

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(LED_VERDE, LED_OFF);
  digitalWrite(LED_AMARILLO, LED_OFF);
  digitalWrite(LED_ROJO, LED_OFF);
  digitalWrite(BUZZER, LOW);

  Serial.println("ESP32 lista - Sistema IoT cinta transportadora");
}

void loop() {
  int lecturaEntrada = digitalRead(SENSOR_ENTRADA);
  int lecturaSalida  = digitalRead(SENSOR_SALIDA);

  int entrada = 0;
  int salida = 0;

  if (lecturaEntrada == SENSOR_ACTIVO) {
    entrada = 1;
  }

  if (lecturaSalida == SENSOR_ACTIVO) {
    salida = 1;
  }

  // Temporizador de alarma
  if (salida == 1) {
    if (contandoSalida == false) {
      tiempoInicioSalida = millis();
      contandoSalida = true;
      alarma = false;
    }

    if (millis() - tiempoInicioSalida >= TIEMPO_ALARMA) {
      alarma = true;
    }
  } else {
    contandoSalida = false;
    alarma = false;
  }

  // Control de LEDs y buzzer
  if (alarma == true) {
    // Estado de alarma: solo rojo + buzzer
    digitalWrite(LED_VERDE, LED_OFF);
    digitalWrite(LED_AMARILLO, LED_OFF);
    digitalWrite(LED_ROJO, LED_ON);
    digitalWrite(BUZZER, HIGH);
  }
  else if (salida == 1) {
    // Objeto detectado en salida: solo amarillo
    digitalWrite(LED_VERDE, LED_OFF);
    digitalWrite(LED_AMARILLO, LED_ON);
    digitalWrite(LED_ROJO, LED_OFF);
    digitalWrite(BUZZER, LOW);
  }
  else if (entrada == 1) {
    // Objeto detectado en entrada: solo verde
    digitalWrite(LED_VERDE, LED_ON);
    digitalWrite(LED_AMARILLO, LED_OFF);
    digitalWrite(LED_ROJO, LED_OFF);
    digitalWrite(BUZZER, LOW);
  }
  else {
    // Nada detectado: todo apagado
    digitalWrite(LED_VERDE, LED_OFF);
    digitalWrite(LED_AMARILLO, LED_OFF);
    digitalWrite(LED_ROJO, LED_OFF);
    digitalWrite(BUZZER, LOW);
  }

  int cinta = 0;

  if (entrada == 1 && salida == 0 && alarma == false) {
    cinta = 1;
  }

  // Enviar datos al panel web
  Serial.print("ENTRADA:");
  Serial.print(entrada);

  Serial.print(";SALIDA:");
  Serial.print(salida);

  Serial.print(";CINTA:");
  Serial.print(cinta);

  Serial.print(";ALARMA:");
  Serial.println(alarma ? 1 : 0);

  delay(300);
}
