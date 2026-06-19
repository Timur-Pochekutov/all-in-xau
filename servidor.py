from flask import Flask, jsonify
import threading

import requests
import time
import os 
from datetime import datetime
from flask_cors import CORS

def ciclo_precio():
    global precio_actual, precio_apertura, maximo, minimo
    fecha_apertura = None
    while True:
        ahora = datetime.now()
        hoy = ahora.date()
        response = requests.get("https://api.gold-api.com/price/XAU")
        precio_actual = response.json()["price"]

        if ahora.hour == 10 and ahora.minute == 0 and fecha_apertura != hoy:
            precio_apertura = precio_actual
            fecha_apertura = hoy
            maximo = precio_actual
            minimo = precio_actual

        if fecha_apertura != hoy and ahora.hour >= 10:
            entrada = input("Precio a las 10:00 ART: ")
            precio_apertura = float(entrada)
            fecha_apertura = hoy
            maximo = precio_apertura
            minimo = precio_apertura

        if precio_apertura is not None:
            if precio_actual > maximo:
                maximo = precio_actual
            if precio_actual < minimo:
                minimo = precio_actual 

        time.sleep(10)

app = Flask(__name__)
CORS(app)

precio_actual = None
precio_apertura = None
maximo = None
minimo = None

@app.route("/precio-sesion")
def precio_sesion():
    cambio = None
    if precio_actual is not None and precio_apertura is not None:
        cambio = round(((precio_actual - precio_apertura) / precio_apertura) * 100, 2)

    return jsonify({
        "precio": precio_actual,
        "apertura": precio_apertura,
        "maximo": maximo,
        "minimo": minimo,
        "cambio_pct": cambio
    })

if __name__ == "__main__":
    hilo = threading.Thread(target=ciclo_precio, daemon=True)
    hilo.start()
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)