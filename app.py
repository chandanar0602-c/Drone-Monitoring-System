from flask import Flask, jsonify, render_template, Response
from telemetry import TelemetrySimulator
from database import init_db, save_snapshot, get_recent, export_csv
from alerts import evaluate_alerts

app = Flask(__name__)
simulator = TelemetrySimulator()
init_db()

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/telemetry")
def api_telemetry():
    data = simulator.next_snapshot()
    alerts = evaluate_alerts(data)
    save_snapshot(data, alerts)
    data["alerts"] = alerts
    return jsonify(data)

@app.route("/api/history")
def api_history():
    return jsonify(get_recent())

@app.route("/api/export")
def api_export():
    return Response(export_csv(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=sky_guardians_logs.csv"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
