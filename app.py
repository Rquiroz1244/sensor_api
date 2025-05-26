from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

# Cargar modelo
with open('modelo_entrenado.pkl', 'rb') as file:
    modelo = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        humedad = float(data['Humedad'])
        luz = float(data['Luminosidad'])
        
        entrada = np.array([[humedad, luz]])
        prediccion = modelo.predict(entrada)[0]

        resultado = {"Temperatura predicha (℃)": round(prediccion, 2)}
        
        # Enviar a webhook de Pipedream
        requests.post(
            "https://eospwhnsj9uhnwv.m.pipedream.net",
            json={
                "humedad": humedad,
                "luz": luz,
                "temperatura": round(prediccion, 2)
            }
        )

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
