import math, random, time
from datetime import datetime
from battery import read_battery
from gps import read_gps
from motors import read_motors
from lidar import read_lidar
from camera import read_camera

class TelemetrySimulator:
    """Demo data generator. All values are simulated, not aircraft measurements."""
    def __init__(self):
        self.tick = 0
        self.started = time.time()
        self.home = {"lat": 12.9716, "lon": 77.5946}

    def next_snapshot(self):
        self.tick += 1
        phases = ["VTOL TAKEOFF", "HOVER", "TRANSITION TO FIXED-WING",
                  "FIXED-WING FLIGHT", "TRANSITION TO VTOL", "VTOL LANDING"]
        phase_index = (self.tick // 20) % len(phases)
        altitude = max(0, 35 + 18 * math.sin(self.tick / 13) + random.uniform(-1.5, 1.5))
        speed = max(0, 12 + 8 * abs(math.sin(self.tick / 17)) + random.uniform(-1, 1))
        lat = self.home["lat"] + 0.0012 * math.sin(self.tick / 30)
        lon = self.home["lon"] + 0.0015 * math.cos(self.tick / 30)
        return {
            "source": "SIMULATED DATA",
            "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
            "connection": "SIMULATION CONNECTED",
            "armed": phase_index not in (0, 5),
            "flight_mode": "AUTO" if phase_index not in (1,) else "LOITER",
            "vtol_phase": phases[phase_index],
            "flight": {
                "altitude_m": round(altitude, 1),
                "ground_speed_ms": round(speed, 1),
                "heading_deg": round((self.tick * 3) % 360, 1),
                "roll_deg": round(4 * math.sin(self.tick / 5), 1),
                "pitch_deg": round(3 * math.cos(self.tick / 7), 1),
                "yaw_deg": round((self.tick * 3) % 360, 1),
                "vertical_speed_ms": round(1.2 * math.cos(self.tick / 13), 1)
            },
            "gps": read_gps(lat, lon, altitude, speed),
            "home": self.home,
            "battery": read_battery(self.tick),
            "motors": read_motors(self.tick),
            "lidar": read_lidar(self.tick),
            "camera": read_camera(),
            "communication": {
                "telemetry": "CONNECTED (SIMULATED)",
                "hm30": "NOT CONNECTED – NO HARDWARE",
                "signal_percent": random.randint(82, 98),
                "latency_ms": random.randint(35, 95),
                "packet_loss_percent": round(random.uniform(0, 1.5), 2),
                "last_packet": datetime.now().strftime("%H:%M:%S")
            },
            "uptime_seconds": int(time.time() - self.started)
        }
