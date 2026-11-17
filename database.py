import sqlite3, csv, io
from pathlib import Path
DB = Path(__file__).parent / "data" / "flight_logs.db"

def connect():
    DB.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS telemetry_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, source TEXT,
            altitude REAL, speed REAL, latitude REAL, longitude REAL,
            battery_percent REAL, battery_voltage REAL, alerts TEXT)""")

def save_snapshot(d, alerts):
    with connect() as con:
        con.execute("""INSERT INTO telemetry_log
        (timestamp, source, altitude, speed, latitude, longitude, battery_percent, battery_voltage, alerts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (d["timestamp"], d["source"], d["flight"]["altitude_m"],
         d["flight"]["ground_speed_ms"], d["gps"]["latitude"], d["gps"]["longitude"],
         d["battery"]["remaining_percent"], d["battery"]["voltage_v"],
         "; ".join(a["message"] for a in alerts)))

def get_recent(limit=100):
    with connect() as con:
        rows = con.execute("SELECT * FROM telemetry_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

def export_csv():
    rows = get_recent(10000)
    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()
