# SKY GUARDIANS – VTOL Drone Monitoring Prototype

## What this build includes
- Flask web dashboard
- Simulated flight telemetry and VTOL phase display
- GPS map and simulated flight path
- Battery voltage/current/percentage and threshold alerts
- Four simulated motor/ESC cards
- Simulated LiDAR distance and sector readings
- Camera integration placeholder (unavailable until real camera/video receiver is connected)
- Simulated communication metrics
- SQLite telemetry history and CSV export

## Important limitations
This is a software demonstration using generated data. It is NOT connected to a drone and does not provide real flight safety, obstacle avoidance, stabilization, or aircraft control. Do not use simulated values for flight decisions. Real camera, HM30, Cube Orange, Jetson, GPS, LiDAR and ESC integration requires the hardware, interface details, and bench validation.

## Setup (Windows PowerShell)
1. Install Python 3.10 or newer and VS Code.
2. Extract this ZIP.
3. Open the `DRONE_MONITORING_SYSTEM` folder in VS Code.
4. Open Terminal > New Terminal.
5. Create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in that terminal:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
   Then activate again.

6. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   python app.py
   ```

8. Open this address in your browser: http://127.0.0.1:5000

## Stop the application
Press `Ctrl + C` in the VS Code terminal.

## Data storage
SQLite database is created automatically at `data/flight_logs.db`.
Use the Export CSV link in the dashboard to download recent stored telemetry.
