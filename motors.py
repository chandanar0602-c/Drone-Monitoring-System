import math
def read_motors(tick):
    result = []
    for i in range(4):
        output = 48 + 12 * abs(math.sin(tick / 8 + i))
        result.append({"id": i + 1, "output_percent": round(output, 1),
                       "rpm": int(4200 + 700 * math.sin(tick / 6 + i)),
                       "temperature_c": round(42 + 5 * abs(math.sin(tick / 11 + i)), 1),
                       "status": "SIMULATED NORMAL"})
    return result
