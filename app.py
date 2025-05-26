from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Cargar modelo previamente entrenado
model = joblib.load('modelo_rf_temperatura.pkl')

# Ruta de prueba
@app.route('/')
def home():
    return "✅ API de predicción de temperatura funcionando"

# Ruta de predicción
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validación de datos
    if data is None:
        return jsonify({'error': 'No se recibió JSON válido'}), 400

    humedad = data.get('Humedad')
    luz = data.get('Luminosidad')

    if humedad is None or luz is None:
        return jsonify({'error': 'Faltan Humedad o Luminosidad'}), 400

    entrada = np.array([[humedad, luz]])
    prediccion = model.predict(entrada)
    resultado = float(prediccion[0])

    # Enviar a Pipedream
    webhook_url = "https://eospwhnsj9uhnwv.m.pipedream.net"
    payload = {
        "fecha": datetime.now().isoformat(),
        "humedad": humedad,
        "luz": luz,
        "temperatura_predicha": resultado
    }

    try:
        requests.post(webhook_url, json=payload, timeout=3)
    except Exception as e:
        print(f"Error enviando a Pipedream: {e}")

    return jsonify({'Temperatura predicha (°C)': resultado})

# Adaptado para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
