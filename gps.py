def read_gps(lat, lon, altitude, speed):
    return {"latitude": round(lat, 7), "longitude": round(lon, 7),
            "altitude_m": round(altitude, 1), "satellites": 14,
            "fix": "3D FIX (SIMULATED)", "ground_speed_ms": round(speed, 1),
            "heading_deg": round((speed * 7) % 360, 1)}
