
def evaluate_alerts(data):
    """
    Evaluate simulated drone monitoring data and generate alerts.
    This module monitors conditions only; it does not control the drone.
    """

    alerts = []
    timestamp = data.get("timestamp", "TIME UNAVAILABLE")

    def add_alert(level, message):
        alerts.append({
            "level": level,
            "message": message,
            "time": timestamp
        })

    # 1. Battery monitoring
    battery = data.get("battery") or {}
    battery_percent = battery.get("remaining_percent")

    if isinstance(battery_percent, (int, float)):
        if battery_percent <= 12:
            add_alert("CRITICAL", "Critical battery level")
        elif battery_percent <= 25:
            add_alert("WARNING", "Low battery level")

    # 2. LiDAR / obstacle monitoring
    lidar = data.get("lidar") or {}
    front_distance = lidar.get("front_distance_m")

    if isinstance(front_distance, (int, float)):
        if front_distance < 2.0:
            add_alert(
                "CRITICAL",
                "Simulated front obstacle detected within 2 metres"
            )
        elif front_distance < 3.0:
            add_alert(
                "WARNING",
                "Simulated front obstacle detected within 3 metres"
            )

    # 3. GPS monitoring
    gps = data.get("gps") or {}
    gps_fix = str(gps.get("fix", "")).upper()
    satellites = gps.get("satellites")

    if "NO GPS FIX" in gps_fix or "INVALID" in gps_fix:
        add_alert("CRITICAL", "GPS fix unavailable")
    elif isinstance(satellites, (int, float)) and satellites < 6:
        add_alert("WARNING", "Weak GPS satellite signal")

    # 4. Motor / ESC monitoring
    motors = data.get("motors") or []

    for motor in motors:
        if not isinstance(motor, dict):
            continue

        motor_id = motor.get("id", "Unknown")
        motor_status = str(motor.get("status", "")).upper()
        temperature = motor.get("temperature_c")

        if "CRITICAL" in motor_status:
            add_alert(
                "CRITICAL",
                f"Motor {motor_id} reports critical status"
            )
        elif "WARNING" in motor_status:
            add_alert(
                "WARNING",
                f"Motor {motor_id} reports warning status"
            )

        if isinstance(temperature, (int, float)):
            if temperature >= 80:
                add_alert(
                    "CRITICAL",
                    f"Motor {motor_id} temperature is critical"
                )
            elif temperature >= 65:
                add_alert(
                    "WARNING",
                    f"Motor {motor_id} temperature is high"
                )

    # 5. Communication monitoring
    communication = data.get("communication") or {}
    packet_loss = communication.get("packet_loss_percent")

    if isinstance(packet_loss, (int, float)):
        if packet_loss > 10:
            add_alert("CRITICAL", "Very high simulated packet loss")
        elif packet_loss > 5:
            add_alert("WARNING", "High simulated packet loss")

    # 6. Camera monitoring
    camera = data.get("camera") or {}
    camera_status = str(camera.get("status", "")).upper()

    if camera_status in ("ERROR", "FAILED"):
        add_alert("WARNING", "Camera module reports an error")

    # 7. General status
    if not alerts:
        add_alert("INFO", "No active monitoring threshold alerts")

    return alerts
