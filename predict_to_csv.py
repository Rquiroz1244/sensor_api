from influxdb import InfluxDBClient
import pandas as pd
import requests

# Conexión a InfluxDB local
client = InfluxDBClient(host='localhost', port=8086, database='sensores')

# Consulta a los últimos 20 registros
query = "SELECT * FROM lecturas_sensor ORDER BY time DESC LIMIT 20"
result = client.query(query)
points = list(result.get_points())

# Lista para almacenar los datos con predicción
datos = []

for punto in points:
    humedad = punto['Humedad']
    luz = punto['Luminosidad']
    temperatura_real = punto['Temperatura']
    timestamp = punto['time']

    payload = {'Humedad': humedad, 'Luminosidad': luz}

    try:
        res = requests.post("http://localhost:5000/predict", json=payload)
        if res.status_code == 200:
            temperatura_predicha = res.json().get("Temperatura predicha (°C)")
        else:
            temperatura_predicha = None
    except Exception as e:
        print("Error al predecir:", e)
        temperatura_predicha = None

    datos.append({
        "time": timestamp,
        "Humedad": humedad,
        "Luminosidad": luz,
        "Temperatura Real": temperatura_real,
        "Temperatura Predicha": temperatura_predicha
    })

# Guardar en CSV
df = pd.DataFrame(datos)
df.to_csv("resultados.csv", index=False, encoding="utf-8")

print("✅ ¡Archivo resultados.csv generado con éxito!")
