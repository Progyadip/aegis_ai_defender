import joblib
import pandas as pd
import time
import random
import threading
import sys

model = joblib.load("models/classifier.pkl")

feature_columns = [
    'file_access_count',
    'network_conn_count',
    'failed_login_attempts',
    'encrypted_file_events',
    'process_spawn_anomaly',
    'external_ip_connection',
    'privilege_escalation_attempts',
    'anomalous_behavior_score',
    'zero_day_indicator'
]

stop_event = threading.Event()

# Global threat counter
total_threats_detected = 0
total_scans = 0

def simulate_system_metrics():
    return [
        random.randint(10, 300),          # file_access_count
        random.randint(1, 100),           # network_conn_count
        random.randint(0, 15),            # failed_login_attempts
        random.randint(0, 3),             # encrypted_file_events (increased range)
        random.randint(0, 1),             # process_spawn_anomaly (missing before)
        random.randint(0, 1),             # external_ip_connection
        random.randint(0, 1),             # privilege_escalation_attempts
        round(random.uniform(0, 1), 2),   # anomalous_behavior_score
        random.randint(0, 1)              # zero_day_indicator
    ]

def scanner():
    global total_threats_detected, total_scans
    while not stop_event.is_set():
        features = pd.DataFrame([simulate_system_metrics()], columns=feature_columns)
        prediction = model.predict(features)[0]
        total_scans += 1

        if prediction == 1:
            total_threats_detected += 1
        
        print("\n[+] Scan #", total_scans)
        print(features.to_string(index=False))
        print("[!] Threat Detected!" if prediction == 1 else "[+] System Safe.")
        print(f"Total threats detected so far: {total_threats_detected}")

        for _ in range(10):
            if stop_event.is_set():
                break
            time.sleep(0.5)

def main():
    print("[+] Aegis AI Defender live scanner started — press 'q' then Enter to stop.")

    thread = threading.Thread(target=scanner, daemon=True)
    thread.start()

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
