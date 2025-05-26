import time
import pandas as pd
import requests
from influxdb import InfluxDBClient

API_URL = 'http://localhost:5000/predict'
client = InfluxDBClient(host='localhost', port=8086, database='sensores')

def obtener_ultimas_lecturas():
    query = 'SELECT * FROM lecturas_sensor ORDER BY time DESC LIMIT 10'
    resultados = client.query(query)
    return list(resultados.get_points())

def predecir_temperatura(humedad, luz):
    try:
        res = requests.post(API_URL, json={"Humedad": humedad, "Luminosidad": luz})
        if res.status_code == 200:
            return res.json().get("Temperatura predicha (°C)")
    except:
        return None

def main():
    registros = []

    while True:
        lecturas = obtener_ultimas_lecturas()
        for punto in reversed(lecturas):
            tiempo = punto['time']
            humedad = punto['Humedad']
            luz = punto['Luminosidad']
            pred = predecir_temperatura(humedad, luz)
            if pred is not None:
                registros.append({
                    "time": tiempo,
                    "Humedad": humedad,
                    "Luminosidad": luz,
                    "Temperatura Predicha": round(pred, 2)
                })

        df = pd.DataFrame(registros).drop_duplicates(subset=["time"])
        df.to_csv("resultados.csv", index=False)
        print(f"✅ actualizado ({len(df)} registros)")
        time.sleep(5)

if __name__ == "__main__":
    main()
