from flask import Flask, jsonify, render_template_string
import serial
import threading
import time

app = Flask(__name__)

PUERTO = "/dev/ttyUSB0"
VELOCIDAD = 115200

datos = {
    "entrada": "-",
    "salida": "-",
    "cinta": "-",
    "alarma": "-",
    "estado": "Esperando conexión",
    "ultima_linea": "-"
}

def procesar_linea(linea):
    partes = linea.split(";")
    resultado = {}

    for parte in partes:
        if ":" in parte:
            clave, valor = parte.split(":", 1)
            resultado[clave.strip().upper()] = valor.strip()

    return resultado

def leer_esp32():
    global datos

    while True:
        try:
            esp32 = serial.Serial(PUERTO, VELOCIDAD, timeout=1)
            time.sleep(2)

            datos["estado"] = "ESP32 conectada"

            while True:
                linea = esp32.readline().decode("utf-8", errors="ignore").strip()

                if linea:
                    valores = procesar_linea(linea)

                    datos["entrada"] = valores.get("ENTRADA", datos["entrada"])
                    datos["salida"] = valores.get("SALIDA", datos["salida"])
                    datos["cinta"] = valores.get("CINTA", datos["cinta"])
                    datos["alarma"] = valores.get("ALARMA", datos["alarma"])
                    datos["ultima_linea"] = linea
                    datos["estado"] = "Recibiendo datos correctamente"

        except Exception as e:
            datos["estado"] = "Error: " + str(e)
            time.sleep(2)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel IoT ESP32</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111;
            color: white;
            text-align: center;
            padding: 30px;
        }

        h1 {
            color: #00ff99;
        }

        .contenedor {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            max-width: 800px;
            margin: auto;
        }

        .tarjeta {
            background: #222;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 0 10px #00ff99;
        }

        .valor {
            font-size: 38px;
            color: #00ff99;
            font-weight: bold;
        }

        .alarma-activa {
            color: red;
        }

        .estado {
            margin-top: 25px;
            padding: 15px;
            background: #333;
            border-radius: 10px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>

    <h1>Panel IoT - Cinta Transportadora ESP32</h1>

    <div class="contenedor">
        <div class="tarjeta">
            <h2>Sensor Entrada</h2>
            <div class="valor" id="entrada">-</div>
        </div>

        <div class="tarjeta">
            <h2>Sensor Salida</h2>
            <div class="valor" id="salida">-</div>
        </div>

        <div class="tarjeta">
            <h2>Estado Cinta</h2>
            <div class="valor" id="cinta">-</div>
        </div>

        <div class="tarjeta">
            <h2>Alarma</h2>
            <div class="valor" id="alarma">-</div>
        </div>
    </div>

    <div class="estado">
        <h3>Estado del sistema</h3>
        <p id="estado">Esperando...</p>
        <p><b>Última línea recibida:</b></p>
        <p id="ultima_linea">-</p>
    </div>

    <script>
        function actualizarDatos() {
            fetch("/datos")
                .then(response => response.json())
                .then(data => {
                    document.getElementById("entrada").innerText = data.entrada;
                    document.getElementById("salida").innerText = data.salida;

                    if (data.cinta == "1") {
                        document.getElementById("cinta").innerText = "ACTIVA";
                    } else if (data.cinta == "0") {
                        document.getElementById("cinta").innerText = "DETENIDA";
                    } else {
                        document.getElementById("cinta").innerText = "-";
                    }

                    const alarmaElemento = document.getElementById("alarma");

                    if (data.alarma == "1") {
                        alarmaElemento.innerText = "ACTIVA";
                        alarmaElemento.classList.add("alarma-activa");
                    } else if (data.alarma == "0") {
                        alarmaElemento.innerText = "NORMAL";
                        alarmaElemento.classList.remove("alarma-activa");
                    } else {
                        alarmaElemento.innerText = "-";
                        alarmaElemento.classList.remove("alarma-activa");
                    }

                    document.getElementById("estado").innerText = data.estado;
                    document.getElementById("ultima_linea").innerText = data.ultima_linea;
                });
        }

        setInterval(actualizarDatos, 500);
        actualizarDatos();
    </script>

</body>
</html>
"""

@app.route("/")
def inicio():
    return render_template_string(html)

@app.route("/datos")
def obtener_datos():
    return jsonify(datos)

if __name__ == "__main__":
    hilo = threading.Thread(target=leer_esp32)
    hilo.daemon = True
    hilo.start()

    app.run(host="0.0.0.0", port=5000)
