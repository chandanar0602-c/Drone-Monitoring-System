
import math


# SIMULATION CONFIGURATION
BATTERY_CAPACITY_MAH = 12000
BATTERY_CELLS = 6
LOW_BATTERY_THRESHOLD = 25
CRITICAL_BATTERY_THRESHOLD = 12


def read_battery(tick):

    # Simulated remaining battery percentage
    percent = max(8, 96 - tick * 0.035)

    # Approximate voltage for a simulated 6S battery
    voltage = 19.8 + (25.2 - 19.8) * (percent / 100)

    # Simulated current consumption
    current = 18 + 4 * abs(math.sin(tick / 9))

    # Remaining capacity
    remaining_capacity = (
        BATTERY_CAPACITY_MAH * percent / 100
    )

    # Power consumption
    power = voltage * current

    # Estimated remaining time using current draw
    if current > 0:
        estimated_minutes = (
            remaining_capacity / 1000
        ) / current * 60
    else:
        estimated_minutes = None

    # Battery health status
    if percent <= CRITICAL_BATTERY_THRESHOLD:
        status = "CRITICAL"

    elif percent <= LOW_BATTERY_THRESHOLD:
        status = "LOW"

    else:
        status = "NORMAL"

    return {
        "voltage_v": round(voltage, 2),
        "current_a": round(current, 2),
        "power_w": round(power, 2),
        "remaining_percent": round(percent, 1),
        "remaining_capacity_mah": round(
            remaining_capacity
        ),
        "total_capacity_mah": BATTERY_CAPACITY_MAH,
        "estimated_minutes": round(estimated_minutes, 1)
        if estimated_minutes is not None else None,
        "status": status,
        "source": "SIMULATED DATA"
    }
