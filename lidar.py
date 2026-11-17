
import math
import random

# SIMULATION THRESHOLDS
WARNING_DISTANCE = 3.0
CRITICAL_DISTANCE = 2.0


def read_lidar(tick):

    # Generate simulated distance readings
    front = 5.5 + 2.2 * math.sin(tick / 6) + random.uniform(-0.2, 0.2)

    front = max(0.4, front)

    sectors = {
        "front": round(front, 2),
        "front_right": round(4.8 + random.random(), 2),
        "right": round(6 + random.random(), 2),
        "rear": round(7 + random.random(), 2),
        "left": round(5 + random.random(), 2),
        "front_left": round(4.5 + random.random(), 2)
    }

    # Classify front obstacle distance
    if front < CRITICAL_DISTANCE:
        obstacle_status = "CRITICAL"

    elif front < WARNING_DISTANCE:
        obstacle_status = "WARNING"

    else:
        obstacle_status = "CLEAR"

    # Check whether any sector contains a nearby obstacle
    obstacle_detected = any(
        distance < WARNING_DISTANCE
        for distance in sectors.values()
    )

    # Return LiDAR information
    return {
        "sensor_status": "SIMULATED",
        "source": "SIMULATED DATA",
        "front_distance_m": round(front, 2),
        "obstacle_detected": obstacle_detected,
        "obstacle_status": obstacle_status,
        "sectors": sectors
    }
