
import math

# SIMULATION CONFIGURATION
RPM_WARNING = 3000
RPM_CRITICAL = 2000

TEMP_WARNING = 60
TEMP_CRITICAL = 75

OUTPUT_WARNING = 90


def read_motors(tick):

    result = []

    # Generate simulated readings for four motors
    for i in range(4):

        output = 48 + 12 * abs(math.sin(tick / 8 + i))

        rpm = int(
            4200 + 700 * math.sin(tick / 6 + i)
        )

        temperature = round(
            42 + 5 * abs(math.sin(tick / 11 + i)), 1
        )

        # Motor health evaluation
        if rpm <= RPM_CRITICAL or temperature >= TEMP_CRITICAL:
            status = "CRITICAL"

        elif (
            rpm <= RPM_WARNING
            or temperature >= TEMP_WARNING
            or output >= OUTPUT_WARNING
        ):
            status = "WARNING"

        else:
            status = "NORMAL"

        result.append({
            "id": i + 1,
            "output_percent": round(output, 1),
            "rpm": rpm,
            "temperature_c": temperature,
            "status": status,
            "source": "SIMULATED DATA"
        })

    # Check RPM imbalance between motors
    average_rpm = sum(m["rpm"] for m in result) / len(result)

    for motor in result:

        difference = abs(motor["rpm"] - average_rpm)

        if average_rpm > 0 and difference / average_rpm > 0.15:
            motor["status"] = "WARNING"

    return result
