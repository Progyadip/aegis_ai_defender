# utils/feature_extractor.py
def extract_features(metrics):
    features = [
        metrics['cpu_usage'],
        metrics['mem_usage'],
        metrics['disk_usage'],
        metrics['net_io_sent'] / 1e6,
        metrics['net_io_recv'] / 1e6,
    ]
    return features
