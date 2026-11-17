
# 🚁 SKY GUARDIANS
## VTOL Drone Monitoring System

A web-based Ground Control Monitoring prototype designed to demonstrate flight telemetry, GPS tracking, battery health, motor monitoring, LiDAR readings, communication status and system alerts.

**Project Type:** Software-only prototype  
**Backend:** Python and Flask  
**Frontend:** HTML, CSS and JavaScript  
**Database:** SQLite  
**Current Mode:** Simulation

---

## 1. Project Overview

Sky Guardians is a VTOL drone monitoring prototype that provides a centralized dashboard for observing simulated aircraft telemetry and subsystem information.

The system generates demonstration data and displays it through a web-based Ground Control Station.

No physical drone or monitoring hardware is connected in this build.

## 2. Features

### Flight Monitoring
- Simulated altitude and ground speed
- Heading, roll, pitch and yaw
- Flight mode and VTOL phase display
- Simulated aircraft status

### GPS Monitoring
- GPS coordinates
- Satellite count and GPS fix status
- Interactive Leaflet map
- Simulated drone movement and flight path

### Battery Monitoring
- Battery voltage
- Current consumption
- Remaining battery percentage
- Estimated remaining capacity
- Estimated flight time
- Low and critical battery alerts

### Motor and ESC Monitoring
- Four simulated motors
- Motor output percentage
- RPM readings
- Temperature monitoring
- Motor health alerts

### LiDAR Monitoring
- Simulated front distance
- Six directional distance sectors
- Obstacle threshold alerts

### Camera Monitoring
- C20 camera integration placeholder
- SIYI HM30 video integration point
- Explicit unavailable status when hardware is disconnected

### Communication Monitoring
- Simulated telemetry connection
- Signal strength
- Communication latency
- Packet loss percentage

### Alerts and Flight Logs
- Battery alerts
- GPS alerts
- Motor alerts
- LiDAR alerts
- Communication alerts
- SQLite telemetry history
- CSV export

## 3. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Web Framework | Flask |
| Real-time communication support | Flask-SocketIO |
| Drone communication integration point | PyMAVLink |
| Serial communication integration point | PySerial |
| Frontend | HTML, CSS, JavaScript |
| Interactive Map | Leaflet |
| Charts | Chart.js |
| Database | SQLite |

## 4. Project Structure

```text
DRONE_MONITORING_SYSTEM/
│
├── app.py
├── telemetry.py
├── alerts.py
├── battery.py
├── gps.py
├── motors.py
├── lidar.py
├── camera.py
├── database.py
│
├── data/
│   └── flight_logs.db
│
├── templates/
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database is generated automatically when the application runs.

## 5. Installation and Setup

### Requirements
- Windows 10 or Windows 11
- Python 3.10 or newer
- Visual Studio Code
- Internet connection for external map tiles and CDN resources

### Step 1: Open the project

Extract the project ZIP file and open the `DRONE_MONITORING_SYSTEM` folder in VS Code.

### Step 2: Open the terminal

Select:

`Terminal → New Terminal`

### Step 3: Create a virtual environment

```powershell
py -3 -m venv .venv
```

### Step 4: Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Step 5: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 6: Start the application

```powershell
python app.py
```

### Step 7: Open the dashboard

Open your browser and visit:

http://127.0.0.1:5000

## 6. API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Main monitoring dashboard |
| `/api/health` | Application health status |
| `/api/telemetry` | Current simulated telemetry |
| `/api/history` | Recent telemetry history |
| `/api/export` | Download telemetry as CSV |

## 7. Database

The application uses SQLite for telemetry storage.

Database location:

```text
data/flight_logs.db
```

The database stores:
- Timestamp
- Data source
- Altitude
- Ground speed
- GPS coordinates
- Battery percentage
- Battery voltage
- Alert messages

The dashboard provides a CSV export option for stored telemetry.

## 8. Important Limitations and Safety

This is a software demonstration using generated data.

It is NOT connected to a physical drone.

The prototype does not provide:
- Real aircraft measurements
- Flight stabilization
- Aircraft control
- Real obstacle avoidance
- Verified flight safety functions

Simulated readings must never be used for actual flight decisions.

Real integration with Cube Orange, Jetson Orin Nano, SIYI HM30, C20 camera, GPS, TF02 LiDAR, rotating LiDAR and ESCs requires the actual hardware, interface specifications, implementation and bench validation.

The monitoring dashboard is not a replacement for independent flight-controller safety systems.

## 9. Future Enhancements

- Real flight-controller telemetry integration
- Physical GPS and battery sensor integration
- Live camera and video streaming
- Actual LiDAR sensor integration
- Real communication link monitoring
- Hardware-in-the-loop testing
- Improved historical telemetry analytics

## 10. Team and Project

**Project Name:** Sky Guardians – VTOL Drone Monitoring System

**Project Category:** Drone Monitoring / Ground Control Station

**Implementation:** Python, Flask and Web Technologies

**Build:** Software-only simulation prototype

---

© 2026 Sky Guardians – VTOL Drone Monitoring Prototype
