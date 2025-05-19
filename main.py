from datetime import datetime
import joblib
import pandas as pd
import time
import random
import threading
import sys
import logging

# Configure logging to log threats to file
logging.basicConfig(
    filename='threat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - Threat detected with features: %(message)s'
)

# Load trained model
model = joblib.load("models/classifier.pkl")

# Feature columns (must match training)
COLUMNS = [
    "file_access_count",
    "network_conn_count",
    "failed_login_attempts",
    "encrypted_file_events",
    "anomalous_behavior_score",
    "privilege_escalation_attempts",
    "external_ip_connection",
]

# Stop flag implemented as an Event (thread‑safe)
stop_event = threading.Event()


def simulate_system_metrics():
    # Mock system metrics – replace with real monitoring later.
    return [
        random.randint(10, 300),          # file_access_count
        random.randint(1, 100),           # network_conn_count
        random.randint(0, 15),            # failed_login_attempts
        random.randint(0, 1),             # encrypted_file_events
        round(random.uniform(0, 1), 2),   # anomalous_behavior_score
        random.randint(0, 1),             # privilege_escalation_attempts
        random.randint(0, 1),             # external_ip_connection
    ]


def scanner():
    while not stop_event.is_set():
        features = pd.DataFrame([simulate_system_metrics()], columns=COLUMNS)
        prediction = model.predict(features)[0]

        # For demo, define some dummy threat types & actions based on features or prediction
        if prediction == 1:
            threat_type = "Ransomware Behavior Detected"
            action = "Isolate affected system, run full malware scan, restore backups."
        else:
            threat_type = None
            action = None

        # Log with details (append to file)
        with open("threat_log.txt", "a") as log_file:
            if prediction == 1:
                log_line = f"{datetime.now()} - Threat detected - Type: {threat_type} - Action: {action}\n"
                log_file.write(log_line)

        print("\n[+] Scanning…")
        print(features.to_string(index=False))
        print("[!] Threat Detected!" if prediction == 1 else "[+] System Safe.")

        for _ in range(10):
            if stop_event.is_set():
                break
            time.sleep(0.5)



def main():
    print("[+] Aegis AI Defender live scanner started — press 'q' then Enter to stop.")

    thread = threading.Thread(target=scanner, daemon=True)
    thread.start()

    # Non‑blocking read loop – waits for user to type 'q' + Enter
    try:
        while True:
            if sys.stdin.readline().strip().lower() == "q":
                stop_event.set()
                thread.join()
                print("[+] Scanning stopped by user.")
                break
    except KeyboardInterrupt:
        stop_event.set()
        thread.join()
        print("\n[+] Scanning stopped (KeyboardInterrupt).")


if __name__ == "__main__":
    main()
