import time
import logging
from collections import defaultdict, deque
from sklearn.ensemble import IsolationForest
import requests
import asyncio
from datetime import datetime, timedelta
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import threading
import json

logging.basicConfig(
    filename='anomaly_detector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
GEO_API_KEY = "XXX"
SIEM_URL = "XX"
SIEM_TOKEN = "YOUR_SIEM_TOKEN"
EXPECTED_LOCATION = "Cracow"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"
FPS = 60

app = Flask(__name__)

failed_logins = defaultdict(lambda: deque(maxlen=10))

def fetch_realtime_ip_data(ip):
    """
    Pobiera dane geolokalizacyjne dla podanego adresu IP.
    """
    try:
        response = requests.get(
            f"https://api.ipgeolocation.io/ipgeo?apiKey={GEO_API_KEY}&ip={ip}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Błąd geolokalizacji IP {ip}: {e}")
        return {"city": "Unknown"}

def analyze_logs(log_file):
    """
    Analizuje logi logowania i wykrywa podejrzane zdarzenia.
    """
    anomalies = defaultdict(list)
    X = []
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if "login" in line.lower():
                    parts = line.split()
                    if len(parts) < 6:
                        continue
                    ip = parts[5]
                    geo_data = fetch_realtime_ip_data(ip)
                    city = geo_data.get("city", "Unknown")
                    is_failed = "failed" in line.lower()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if is_failed:
                        now = datetime.now()
                        failed_logins[ip].append(now)
                        recent = [t for t in failed_logins[ip] if now - t < timedelta(minutes=5)]
                        if len(recent) >= 5:
                            event = f"Brute-force: >=5 nieudanych logowań z IP {ip} w 5 minut"
                            anomalies[timestamp].append({"msg": event, "type": "ALERT"})
                            logging.warning(f"[ALERT {timestamp}] {event}")

                    if city != EXPECTED_LOCATION or is_failed:
                        event = f"Podejrzane logowanie z {city}, IP: {ip}"
                        anomalies[timestamp].append({"msg": event, "type": "ALERT"})
                        logging.warning(f"[ALERT {timestamp}] {event}")

                    X.append([int(is_failed), int(city != EXPECTED_LOCATION)])
        return anomalies, X
    except Exception as e:
        logging.error(f"Błąd analizy logów: {e}")
        return anomalies, X

def send_to_siem(anomalies):
    """
    Wysyła alerty do systemu SIEM.
    """
    try:
        payload = {
            "alerts": list(anomalies.items()),
            "timestamp": datetime.now().isoformat()
        }
        headers = {
            "Authorization": f"Bearer {SIEM_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(SIEM_URL, json=payload, headers=headers, timeout=5)
        if response.status_code != 200:
            logging.error(f"Błąd SIEM: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"Błąd połączenia z SIEM: {e}")

def send_alert_email(subject, body):
    """
    Wysyła powiadomienie e-mail o wykrytej anomalii.
    """
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Błąd wysyłki e-mail: {e}")

def train_model(X):
    """
    Trenuje model Isolation Forest na danych z logów.
    """
    if X:
        return IsolationForest(contamination=0.1, random_state=42).fit(X)
    return None

async def monitor_logs():
    """
    Monitoruje logi w czasie rzeczywistym i wykrywa anomalie.
    """
    model = train_model([])
    while True:
        anomalies, X = analyze_logs('login_logs.txt')
        if X and model:
            model.fit(X)
            outliers = model.predict(X)
            for i, (timestamp, events) in enumerate(anomalies.items()):
                if outliers[i] == -1:
                    for event in events:
                        print(f"[Alert {timestamp}] {event['msg']}")
                        send_to_siem({timestamp: [event['msg']]})
                        send_alert_email("Anomalia logowania", event['msg'])
        await asyncio.sleep(1.0 / FPS)

@app.route('/', methods=['GET'])
def dashboard():
    """
    Dashboard webowy z ostatnimi alertami i prostym wykresem.
    """
    logs = []
    alert_hours = defaultdict(int)
    try:
        with open('anomaly_detector.log', 'r') as f:
            for line in f.readlines()[-50:]:
                if "ALERT" in line:
                    logs.append({"msg": line.strip(), "type": "ALERT"})
                    try:
                        hour = line.split()[1][:2]
                        alert_hours[hour] += 1
                    except Exception:
                        pass
                else:
                    logs.append({"msg": line.strip(), "type": "INFO"})
    except Exception:
        logs = [{"msg": "Brak logów lub błąd odczytu.", "type": "INFO"}]
    chart_labels = list(alert_hours.keys())
    chart_values = list(alert_hours.values())
    return render_template('dashboard.html', logs=logs, chart_labels=chart_labels, chart_values=chart_values)

@app.route('/api/ping')
def ping():
    return {"status": "ok"}

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(monitor_logs()), daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)