from flask import Flask, jsonify, request
import threading

import requests
import time
import os 
from datetime import datetime
from zoneinfo import ZoneInfo
from flask_cors import CORS

def ciclo_precio():
    global precio_actual, precio_apertura, maximo, minimo, fecha_apertura
    zona_ar = ZoneInfo("America/Argentina/Buenos_Aires")
    while True:
        ahora = datetime.now(zona_ar)
        hoy = ahora.date()
        response = requests.get("https://api.gold-api.com/price/XAU")
        precio_actual = response.json()["price"]

        if ahora.hour == 10 and ahora.minute == 30 and fecha_apertura != hoy:
            precio_apertura = precio_actual
            fecha_apertura = hoy
            maximo = precio_actual
            minimo = precio_actual

        if precio_apertura is not None:
            if precio_actual > maximo:
                maximo = precio_actual
            if precio_actual < minimo:
                minimo = precio_actual 

        time.sleep(10)
def actualizar_tasas():
    global tasas_cambio, ultima_actualizacion_tasas
    while True:
        try:
            response = requests.get("https://api.frankfurter.dev/v2/rates?base=USD&quotes=EUR,GBP,JPY,AUD")
            data = response.json()

            nuevas_tasas = {}
            for fila in data:
                nuevas_tasas[fila["quote"]] = fila["rate"]

            tasas_cambio = nuevas_tasas
            ultima_actualizacion_tasas = datetime.now()
        except Exception as e:
            print(f"Error actualizando tasas: {e}")

        time.sleep(3600)

FINNHUB_KEY = os.environ.get("FINNHUB_KEY")

def actualizar_etf():
    global datos_etf
    while True:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol=GLD&token={FINNHUB_KEY}"
            response = requests.get(url)
            data = response.json()

            datos_etf = {
                "precio": data["c"],
                "cambio": data["d"],
                "cambio_pct": data["dp"],
                "maximo": data["h"],
                "minimo": data["l"]
            }
        except Exception as e:
            print(f"Error actualizando ETF: {e}")

        time.sleep(60)

app = Flask(__name__)
CORS(app)

precio_actual = None
precio_apertura = None
maximo = None
minimo = None
fecha_apertura = None
tasas_cambio = {}
ultima_actualizacion_tasas = None
precios_mercados = {}
datos_etf = {}

CLAVE_ADMIN = os.environ.get("CLAVE_ADMIN")

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

@app.route("/registrar-apertura")
def registrar_apertura():
    global precio_apertura, maximo, minimo, fecha_apertura
    
    clave = request.args.get("clave")
    if CLAVE_ADMIN is None or clave != CLAVE_ADMIN:
        return jsonify({"error": "no autorizado"}), 403
    
    zona_ar = ZoneInfo("America/Argentina/Buenos_Aires")
    hoy = datetime.now(zona_ar).date()

    forzar = request.args.get("forzar")
    if fecha_apertura == hoy and forzar != "true":
        return jsonify({"error": "la apertura de hoy ya esta registrada, usa &forzar=true para sobreescribir"}), 409

    valor = request.args.get("precio")
    if valor is None:
        return jsonify({"error": "falta el parametro precio"}), 400
    
    precio_apertura = float(valor)
    maximo = precio_apertura
    minimo = precio_apertura
    fecha_apertura = hoy
    return jsonify({"mensaje" : "apertura registrada", "apertura": precio_apertura})

@app.route("/mercados")
def mercados():
    if precio_actual is None or not tasas_cambio:
        return jsonify({
            "USD": None,
            "EUR": None,
            "GBP": None,
            "JPY": None,
            "AUD": None
            }) 
    return jsonify({
        "USD": round(precio_actual, 2),
        "EUR": round(precio_actual * tasas_cambio["EUR"], 2),
        "GBP": round(precio_actual * tasas_cambio["GBP"], 2),
        "JPY": round(precio_actual * tasas_cambio["JPY"], 2),
        "AUD": round(precio_actual * tasas_cambio["AUD"], 2)
        }) 

@app.route("/etf")
def etf():
    if not datos_etf:
        return jsonify({
            "precio": None,
            "cambio": None,
            "cambio_pct": None,
            "maximo": None,
            "minimo": None
        })
    
    return jsonify(datos_etf)

if __name__ == "__main__":
    hilo = threading.Thread(target=ciclo_precio, daemon=True)
    hilo.start()

    hilo_tasas = threading.Thread(target=actualizar_tasas, daemon=True)
    hilo_tasas.start()

    hilo_etf = threading.Thread(target=actualizar_etf, daemon=True)
    hilo_etf.start()
    
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
    