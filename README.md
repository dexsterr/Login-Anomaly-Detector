# 🚨 Login Anomaly Detector

> **EN/PL below**  
> Minimalistyczne narzędzie do wykrywania anomalii logowania i ataków brute-force w czasie rzeczywistym.

---

## 🇬🇧 **Login Anomaly Detector (EN)**

A simple, modular Python tool for real-time detection of suspicious login activity and brute-force attacks using log analysis and machine learning.

---

### ✨ **Features**
- 🔎 **Real-time log analysis**
- 🤖 **Brute-force & anomaly detection** (ML + rules)
- 📧 **SIEM & e-mail alerting**
- 📊 **Web dashboard** with color-coded alerts & chart
- 🧩 **Modular, well-documented code**
- 🧪 **Unit test example & README**

---

### ⚙️ **How does it work?**

1. **Real-time log monitoring:**  
   Continuously analyzes login logs for failed attempts, unusual locations, and brute-force patterns.
2. **Anomaly detection:**  
   Uses Isolation Forest (ML) and custom rules to flag suspicious events.
3. **Alerting:**  
   Sends alerts to SIEM and via e-mail when anomalies are detected.
4. **Web dashboard:**  
   Flask-based dashboard displays recent alerts (color-coded) and a chart of alert frequency.
5. **Logging:**  
   All events are saved to a log file for auditing.
6. **Unit tests:**  
   Includes a sample test for brute-force detection logic.

---

### 🛠️ **Requirements**
- Python 3.12+
- Flask
- scikit-learn
- requests

---

## 🇵🇱 **Login Anomaly Detector (PL)**

Proste, modułowe narzędzie w Pythonie do wykrywania podejrzanych logowań i ataków brute-force w czasie rzeczywistym na podstawie analizy logów i uczenia maszynowego.

---

### ✨ **Funkcje**
- 🔎 **Analiza logów w czasie rzeczywistym**
- 🤖 **Wykrywanie brute-force i anomalii** (ML + reguły)
- 📧 **Alerty do SIEM i e-mail**
- 📊 **Dashboard webowy** z kolorowaniem alertów i wykresem
- 🧩 **Modułowy, dobrze opisany kod**
- 🧪 **Przykładowy test jednostkowy i README**

---

### ⚙️ **Jak to działa?**

1. **Monitorowanie logów w czasie rzeczywistym:**  
   Analizuje logi logowań pod kątem nieudanych prób, nietypowych lokalizacji i wzorców brute-force.
2. **Wykrywanie anomalii:**  
   Wykorzystuje Isolation Forest (ML) oraz własne reguły do flagowania podejrzanych zdarzeń.
3. **Alertowanie:**  
   Wysyła alerty do SIEM oraz na e-mail po wykryciu anomalii.
4. **Dashboard webowy:**  
   Dashboard Flask prezentuje ostatnie alerty (kolorowane) i wykres częstości alertów.
5. **Logowanie:**  
   Wszystkie zdarzenia są zapisywane do pliku logów.
6. **Testy jednostkowe:**  
   Przykładowy test logiki wykrywania brute-force.

---

### 🛠️ **Wymagania**
- Python 3.12+
- Flask
- scikit-learn
- requests

---

## 🌐 **How to connect IP Geolocation API?**

1. **Register** at [ipgeolocation.io](https://ipgeolocation.io/) and get your free API key.
2. **Paste your API key** in `login_anomaly_detector.py`:
   ```python
   GEO_API_KEY = "YOUR_IPGEOLOCATION_API_KEY"
   ```
3. **Restart** your app.

---

**Enjoy! 🚀**