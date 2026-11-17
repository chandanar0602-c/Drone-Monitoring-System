import math, random
def read_lidar(tick):
    front = 5.5 + 2.2 * math.sin(tick / 6) + random.uniform(-0.2, 0.2)
    front = max(0.4, front)
    return {"sensor_status": "SIMULATED",
            "front_distance_m": round(front, 2),
            "obstacle_detected": front < 2.0,
            "sectors": {"front": round(front, 2),
                        "front_right": round(4.8 + random.random(), 2),
                        "right": round(6 + random.random(), 2),
                        "rear": round(7 + random.random(), 2),
                        "left": round(5 + random.random(), 2),
                        "front_left": round(4.5 + random.random(), 2)}}
