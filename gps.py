
def read_gps(lat, lon, altitude, speed,
             satellites=14, fix="3D FIX (SIMULATED)"):

    # Validate GPS coordinates
    valid_coordinates = (
        -90 <= lat <= 90 and
        -180 <= lon <= 180
    )

    if not valid_coordinates:
        return {
            "latitude": None,
            "longitude": None,
            "altitude_m": None,
            "satellites": satellites,
            "fix": "INVALID",
            "ground_speed_ms": None,
            "heading_deg": None,
            "source": "SIMULATED DATA"
        }

    # GPS quality status
    if satellites < 4:
        fix = "NO GPS FIX"
    elif satellites < 6:
        fix = "WEAK GPS FIX"

    return {
        "latitude": round(lat, 7),
        "longitude": round(lon, 7),
        "altitude_m": round(altitude, 1),
        "satellites": satellites,
        "fix": fix,
        "ground_speed_ms": round(speed, 1),
        "heading_deg": round((speed * 7) % 360, 1),
        "source": "SIMULATED DATA"
    }
