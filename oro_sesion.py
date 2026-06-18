import requests
import time
from datetime import datetime

def obtener_precio():
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(url)
    data = response.json()
    return data ["price"]

precio_apertura = None
fecha_apertura = None
maximo = None
minimo = None

while True:
    ahora = datetime.now()
    hoy = ahora.date()
    precio = obtener_precio()

    if ahora.hour == 10 and ahora.minute == 0 and fecha_apertura != hoy:
        precio_apertura = precio
        fecha_apertura = hoy
        maximo = precio 
        minimo = precio 
        print(f"Apertura registrada automaticamente: {precio_apertura}")

    if fecha_apertura != hoy and ahora.hour >= 10:
        entrada = input("No se registro apertura de hoy. Precio a las 10:00 ART: ")
        precio_apertura = float(entrada)
        fecha_apertura = hoy
        maximo = precio_apertura
        minimo = precio_apertura
        print(f"Apertura registrada manualmente: {precio_apertura}")

    if precio_apertura is not None:
        if precio > maximo:
            maximo = precio
        if precio < minimo:
            minimo = precio 
        cambio_pct = ((precio - precio_apertura) / precio_apertura) * 100

        print(f"{ahora.strftime('%H:%M:%S')} | actual: {precio:.2f} | apertura: {precio_apertura:.2f} | max: {maximo:.2f} | min: {minimo:.2f} | cambio: {cambio_pct:+.2f}%")
    else:
        print(f"{ahora.strftime('%H:%M:%S')} | actual: {precio:.2f} | esperando apertura...")

    time.sleep(10)
