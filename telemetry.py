
import math
import random
import time
from datetime import datetime

from battery import read_battery
from gps import read_gps
from motors import read_motors
from lidar import read_lidar
from camera import read_camera


class TelemetrySimulator:
    """
    Generates demonstration telemetry for Sky Guardians.

    IMPORTANT:
    All generated readings are simulated.
    They are not measurements from a real aircraft.
    """

    def __init__(self):
        self.tick = 0
        self.started = time.time()

        # Demonstration home location
        self.home = {
            "lat": 12.9716,
            "lon": 77.5946
        }

        self.phases = [
            "VTOL TAKEOFF",
            "HOVER",
            "TRANSITION TO FIXED-WING",
            "FIXED-WING FLIGHT",
            "TRANSITION TO VTOL",
            "VTOL LANDING"
        ]

    def next_snapshot(self):
        """Generate one complete simulated telemetry snapshot."""

        self.tick += 1

        # Simulated flight phase
        phase_index = (self.tick // 20) % len(self.phases)
        current_phase = self.phases[phase_index]

        # Simulated flight readings
        altitude = max(
            0,
            35 + 18 * math.sin(self.tick / 13)
            + random.uniform(-1.5, 1.5)
        )

        speed = max(
            0,
            12 + 8 * abs(math.sin(self.tick / 17))
            + random.uniform(-1, 1)
        )

        heading = (self.tick * 3) % 360

        roll = 4 * math.sin(self.tick / 5)
        pitch = 3 * math.cos(self.tick / 7)

        vertical_speed = 1.2 * math.cos(self.tick / 13)

        # Simulated GPS movement around home location
        latitude = (
            self.home["lat"]
            + 0.0012 * math.sin(self.tick / 30)
        )

        longitude = (
            self.home["lon"]
            + 0.0015 * math.cos(self.tick / 30)
        )

        # Collect readings from individual modules
        gps_data = read_gps(
            latitude,
            longitude,
            altitude,
            speed
        )

        battery_data = read_battery(self.tick)

        motor_data = read_motors(self.tick)

        lidar_data = read_lidar(self.tick)

        camera_data = read_camera()

        # Simulated communication readings
        communication_data = {
            "telemetry": "CONNECTED (SIMULATED)",
            "hm30": "NOT CONNECTED - NO HARDWARE",
            "signal_percent": random.randint(82, 98),
            "latency_ms": random.randint(35, 95),
            "packet_loss_percent": round(
                random.uniform(0, 1.5), 2
            ),
            "last_packet": datetime.now().astimezone().strftime(
                "%H:%M:%S"
            )
        }

        # Complete telemetry snapshot
        snapshot = {
            "source": "SIMULATED DATA",
            "simulation": True,

            "timestamp": datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),

            "connection": "SIMULATION CONNECTED",

            # This is only a simulated state.
            # It does not arm or control a real aircraft.
            "armed": phase_index not in (0, 5),

            "flight_mode": (
                "LOITER" if phase_index == 1 else "AUTO"
            ),

            "vtol_phase": current_phase,

            "flight": {
                "altitude_m": round(altitude, 1),
                "ground_speed_ms": round(speed, 1),
                "heading_deg": round(heading, 1),
                "roll_deg": round(roll, 1),
                "pitch_deg": round(pitch, 1),
                "yaw_deg": round(heading, 1),
                "vertical_speed_ms": round(
                    vertical_speed, 1
                )
            },

            "gps": gps_data,

            "home": self.home.copy(),

            "battery": battery_data,

            "motors": motor_data,

            "lidar": lidar_data,

            "camera": camera_data,

            "communication": communication_data,

            "uptime_seconds": int(
                time.time() - self.started
            )
        }

        return snapshot
