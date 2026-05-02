from flask import Flask, render_template, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Infos de l'app exposées dans Prometheus
metrics.info('app_info', 'Tracker vélos', version='1.0.0')

JCDECAUX_API = "https://api.jcdecaux.com/vls/v1/stations"
API_KEY = os.environ.get("JCDECAUX_API_KEY", "")
CONTRACT = os.environ.get("JCDECAUX_CONTRACT", "paris")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stations")
def stations():
    try:
        params = {"contract": CONTRACT, "apiKey": API_KEY}
        response = requests.get(JCDECAUX_API, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # On nettoie et simplifie les données envoyées au frontend
        stations = []
        for s in data:
            if s.get("position"):
                stations.append({
                    "name": s["name"],
                    "lat": s["position"]["lat"],
                    "lng": s["position"]["lng"],
                    "available_bikes": s.get("available_bikes", 0),
                    "available_bike_stands": s.get("available_bike_stands", 0),
                    "status": s.get("status", "CLOSED")
                })
        return jsonify(stations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "velov-tracker"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
