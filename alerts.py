def evaluate_alerts(data):
    alerts = []
    battery = data["battery"]["remaining_percent"]
    if battery <= 12:
        alerts.append({"level": "CRITICAL", "message": "Critical battery threshold"})
    elif battery <= 25:
        alerts.append({"level": "WARNING", "message": "Low battery threshold"})
    if data["lidar"]["front_distance_m"] < 2:
        alerts.append({"level": "WARNING", "message": "Simulated obstacle within 2 metres"})
    if data["communication"]["packet_loss_percent"] > 5:
        alerts.append({"level": "WARNING", "message": "High simulated packet loss"})
    if not alerts:
        alerts.append({"level": "INFO", "message": "No active threshold alerts"})
    return [{"level": a["level"], "message": a["message"], "time": data["timestamp"]} for a in alerts]
