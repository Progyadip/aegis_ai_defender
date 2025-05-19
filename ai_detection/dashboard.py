from datetime import datetime
from collections import defaultdict
import os
from flask import Flask, jsonify, render_template

# Define correct absolute template path
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
# Path to the log file
LOG_FILE = "threat_log.txt"

# Function to parse logs
def parse_logs():
    if not os.path.exists(LOG_FILE):
        return []

    threats = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            if "Threat detected" in line:
                try:
                    timestamp_str = line.split(' - ')[0]
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                    parts = line.strip().split(" - ")
                    threat_type = None
                    action = None
                    for part in parts:
                        if part.startswith("Type:"):
                            threat_type = part.replace("Type:", "").strip()
                        if part.startswith("Action:"):
                            action = part.replace("Action:", "").strip()
                    threats.append({
                        "timestamp": timestamp,
                        "threat_type": threat_type,
                        "action": action,
                    })
                except Exception:
                    pass
    return threats




# Route: Dashboard HTML
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# API Route: Total threats count
@app.route('/api/threats')
def get_threat_count():
    threats = parse_logs()
    return jsonify({"count": len(threats)})

# API Route: Hourly stats
@app.route('/api/threats/stats')
def get_threat_stats():
    threats = parse_logs()
    hourly_counts = defaultdict(int)
    for t in threats:
        hour_label = t["timestamp"].strftime("%Y-%m-%d %H:00")
        hourly_counts[hour_label] += 1
    return jsonify({"hourly_counts": dict(hourly_counts)})

# API Route: Detailed threat list
@app.route('/api/threats/detailed')
def get_threats_detailed():
    threats = parse_logs()
    threats_sorted = sorted(threats, key=lambda x: x["timestamp"], reverse=True)
    for t in threats_sorted:
        t["timestamp"] = t["timestamp"].isoformat()
    return jsonify(threats_sorted)

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
