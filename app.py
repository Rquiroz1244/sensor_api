from flask import Flask, request, jsonify
import joblib
import numpy as np
import os  # Necesario para leer el puerto desde la variable de entorno

app = Flask(__name__)

# Cargar el modelo
model = joblib.load('modelo_rf_temperatura.pkl')

# Ruta principal
@app.route('/')
def home():
    return "✅ API de predicción de temperatura funcionando"

# Ruta de predicción
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validación básica del JSON recibido
    if data is None:
        return jsonify({'error': 'No se recibió JSON válido'}), 400

    humedad = data.get('Humedad')
    luz = data.get('Luminosidad')

    if humedad is None or luz is None:
        return jsonify({'error': 'Faltan Humedad o Luminosidad'}), 400

    entrada = np.array([[humedad, luz]])
    prediccion = model.predict(entrada)

    return jsonify({'Temperatura predicha (°C)': float(prediccion[0])})

# Punto de entrada adaptado a Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render define este puerto automáticamente
    app.run(host='0.0.0.0', port=port)


