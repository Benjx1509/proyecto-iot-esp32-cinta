# Proyecto IoT ESP32 - Cinta Transportadora

**Estudiante:** Benjamin Pozo  
**Correo:** benjapozopalma@gmail.com  

## Descripción del proyecto

Este proyecto representa una maqueta funcional de una cinta transportadora industrial utilizando una ESP32, dos sensores digitales, tres LEDs, un buzzer y una interfaz web local desarrollada con Python Flask.

La ESP32 detecta el estado de los sensores, controla salidas visuales y sonoras, y envía los datos mediante comunicación serial USB hacia una máquina virtual AmogOS-Debian. En la máquina virtual se ejecuta un programa en Python con Flask que muestra los estados del sistema en una página web local.

## Componentes utilizados

- ESP32 Dev Module
- 2 sensores digitales
- 3 LEDs: verde, amarillo y rojo
- 1 buzzer
- Resistencias para LEDs
- Protoboard
- Cables Dupont
- AmogOS-Debian en VirtualBox
- Python Flask

## Funcionamiento del sistema

- Si el sensor de entrada detecta un objeto, se enciende el LED verde.
- Si el sensor de salida detecta un objeto, se apaga el LED verde y se enciende el LED amarillo.
- Si el sensor de salida permanece activado durante 5 segundos, se apaga el LED amarillo y se activa la alarma.
- La alarma enciende el LED rojo y activa el buzzer.
- La ESP32 envía los estados del sistema al panel web mediante comunicación serial USB.

## Pines utilizados

| Componente | Pin ESP32 |
|---|---|
| Sensor entrada | GPIO 18 |
| Sensor salida | GPIO 19 |
| LED verde | GPIO 23 |
| LED amarillo | GPIO 22 |
| LED rojo | GPIO 21 |
| Buzzer | GPIO 25 |
| Alimentación sensores | 3.3 V |
| Tierra común | GND |

## Datos enviados por la ESP32

La ESP32 envía datos por comunicación serial en este formato:

```text
ENTRADA:1;SALIDA:0;CINTA:1;ALARMA:0
