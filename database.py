
import sqlite3
import csv
import io
from pathlib import Path

# Database location
DB = Path(__file__).parent / "data" / "flight_logs.db"


def connect():
    """Create the database folder and connect to SQLite."""

    DB.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    """Create the telemetry table if it does not already exist."""

    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source TEXT,
                altitude REAL,
                speed REAL,
                latitude REAL,
                longitude REAL,
                battery_percent REAL,
                battery_voltage REAL,
                alerts TEXT
            )
        """)


def save_snapshot(data, alerts):
    """Save one telemetry snapshot and its alerts."""

    flight = data.get("flight") or {}
    gps = data.get("gps") or {}
    battery = data.get("battery") or {}

    alert_messages = "; ".join(
        alert.get("message", "Unknown alert")
        for alert in alerts
    )

    with connect() as con:
        con.execute("""
            INSERT INTO telemetry_log (
                timestamp,
                source,
                altitude,
                speed,
                latitude,
                longitude,
                battery_percent,
                battery_voltage,
                alerts
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("timestamp"),
            data.get("source", "UNKNOWN"),
            flight.get("altitude_m"),
            flight.get("ground_speed_ms"),
            gps.get("latitude"),
            gps.get("longitude"),
            battery.get("remaining_percent"),
            battery.get("voltage_v"),
            alert_messages
        ))


def get_recent(limit=100):
    """Return the most recent telemetry records."""

    limit = max(1, min(int(limit), 10000))

    with connect() as con:
        rows = con.execute(
            """
            SELECT *
            FROM telemetry_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        return [dict(row) for row in rows]


def export_csv():
    """Export telemetry history as CSV text."""

    rows = get_recent(10000)

    output = io.StringIO()

    if rows:
        writer = csv.DictWriter(
            output,
            fieldnames=list(rows[0].keys())
        )

        writer.writeheader()
        writer.writerows(rows)

    return output.getvalue()
