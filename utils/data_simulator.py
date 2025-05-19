import random
import time

def simulate_ransomware_activity():
    # Simulate file encryption spikes
    file_encrypt_events = random.choice([0, 0, 1, 2, 3, 5])  # spikes on ransomware attack
    process_spawn_anomaly = random.choice([0, 1])  # suspicious processes
    external_connections = random.choice([0, 1])
    privilege_escalation = random.choice([0, 1])
    anomalous_behavior_score = round(random.uniform(0, 1), 2)
    zero_day_indicator = random.choice([0, 0, 0, 1])  # rare zero-day sign

    return {
        'file_access_count': random.randint(50, 300),
        'network_conn_count': random.randint(10, 100),
        'failed_login_attempts': random.randint(0, 10),
        'encrypted_file_events': file_encrypt_events,
        'process_spawn_anomaly': process_spawn_anomaly,
        'external_ip_connection': external_connections,
        'privilege_escalation_attempts': privilege_escalation,
        'anomalous_behavior_score': anomalous_behavior_score,
        'zero_day_indicator': zero_day_indicator
    }
