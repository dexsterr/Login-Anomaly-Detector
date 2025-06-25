from login_anomaly_detector import analyze_logs

def test_analyze_logs_brute_force():
    log_content = "\n".join([
        "2025-01-25 login failed 192.168.1.1 user1",
        "2025-01-25 login failed 192.168.1.1 user1",
        "2025-01-25 login failed 192.168.1.1 user1",
        "2025-01-25 login failed 192.168.1.1 user1",
        "2025-01-25 login failed 192.168.1.1 user1"
    ])
    with open("login_logs.txt", "w") as f:
        f.write(log_content)
    anomalies, X = analyze_logs("login_logs.txt")
    assert any("Brute-force" in event["msg"] for events in anomalies.values() for event in events)