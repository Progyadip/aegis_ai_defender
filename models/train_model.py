import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Sample data generation for training
def generate_training_data(n=1000):
    import random
    data = []
    for _ in range(n):
        file_access_count = random.randint(10, 300)
        network_conn_count = random.randint(1, 100)
        failed_login_attempts = random.randint(0, 15)
        encrypted_file_events = random.randint(0, 1)
        anomalous_behavior_score = round(random.uniform(0, 1), 2)
        privilege_escalation_attempts = random.randint(0, 1)
        external_ip_connection = random.randint(0, 1)

        # Simple logic for threat: 1 if many failed attempts or encrypted events
        threat = 1 if (failed_login_attempts > 5 or encrypted_file_events == 1) else 0

        data.append([
            file_access_count,
            network_conn_count,
            failed_login_attempts,
            encrypted_file_events,
            anomalous_behavior_score,
            privilege_escalation_attempts,
            external_ip_connection,
            threat
        ])

    columns = [
        'file_access_count',
        'network_conn_count',
        'failed_login_attempts',
        'encrypted_file_events',
        'anomalous_behavior_score',
        'privilege_escalation_attempts',
        'external_ip_connection',
        'threat'
    ]

    return pd.DataFrame(data, columns=columns)

def train_and_save_model():
    df = generate_training_data(1000)
    X = df.drop('threat', axis=1)
    y = df['threat']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    print(f"Training accuracy: {clf.score(X_train, y_train):.2f}")
    print(f"Test accuracy: {clf.score(X_test, y_test):.2f}")

    # Save the model
    joblib.dump(clf, 'classifier.pkl')
    print("Model saved as classifier.pkl")

if __name__ == "__main__":
    train_and_save_model()
