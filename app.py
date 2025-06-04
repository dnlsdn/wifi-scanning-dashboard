# app.py
from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)
# Percorso assoluto al file dei pacchetti per evitare problemi se l'app viene
# avviata da una directory differente dal progetto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "wifi_packets.csv")

def read_latest(n=50):
    """
    Legge il file CSV e restituisce le ultime n righe (escludendo l'header).
    Ogni riga viene restituita come lista di valori [timestamp, mac, bssid, ssid, rssi, channel].
    """
    rows = []
    if not os.path.isfile(DATA_FILE):
        return rows

    with open(DATA_FILE, newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # Salta l'header
        for row in reader:
            rows.append(row)
    # Ritorna le ultime n righe
    return rows[-n:]

@app.route("/data")
def data():
    # Legge le ultime 50 righe e le invia come JSON
    latest = read_latest(50)
    return jsonify(latest)

@app.route("/")
def index():
    # Mostra il template index.html
    return render_template("index.html")

if __name__ == "__main__":
    # Il server sarà accessibile da 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
