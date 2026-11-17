import math
def read_battery(tick):
    percent = max(8, 96 - tick * 0.035)
    voltage = 25.2 * percent / 100 + 3.0
    current = 18 + 4 * abs(math.sin(tick / 9))
    capacity = 12000
    status = "NORMAL" if percent > 25 else ("LOW" if percent > 12 else "CRITICAL")
    return {
        "voltage_v": round(voltage, 2), "current_a": round(current, 2),
        "remaining_percent": round(percent, 1),
        "remaining_capacity_mah": round(capacity * percent / 100),
        "total_capacity_mah": capacity,
        "estimated_minutes": round(percent * 0.55), "status": status
    }
