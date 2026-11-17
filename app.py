
from flask import Flask, jsonify, render_template, Response
from telemetry import TelemetrySimulator
from database import init_db, save_snapshot, get_recent, export_csv
from alerts import evaluate_alerts

app = Flask(__name__)

# Initialize telemetry simulator
simulator = TelemetrySimulator()

# Initialize database
init_db()


@app.route("/")
def index():
    """Display the main monitoring dashboard."""
    return render_template("dashboard.html")


@app.route("/api/telemetry")
def api_telemetry():
    """Generate telemetry, evaluate alerts and save a snapshot."""

    try:
        data = simulator.next_snapshot()

        alerts = evaluate_alerts(data)

        save_snapshot(data, alerts)

        data["alerts"] = alerts

        return jsonify(data)

    except Exception as error:
        app.logger.exception("Telemetry API error")

        return jsonify({
            "error": "Unable to retrieve telemetry",
            "details": str(error)
        }), 500


@app.route("/api/history")
def api_history():
    """Return recent monitoring history."""

    try:
        return jsonify(get_recent())

    except Exception as error:
        app.logger.exception("History API error")

        return jsonify({
            "error": "Unable to retrieve history",
            "details": str(error)
        }), 500


@app.route("/api/export")
def api_export():
    """Download telemetry history as a CSV file."""

    try:
        return Response(
            export_csv(),
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=sky_guardians_logs.csv"
            }
        )

    except Exception as error:
        app.logger.exception("CSV export error")

        return jsonify({
            "error": "Unable to export telemetry",
            "details": str(error)
        }), 500


@app.route("/api/health")
def api_health():
    """Check whether the monitoring application is running."""

    return jsonify({
        "application": "Sky Guardians Drone Monitoring System",
        "status": "RUNNING",
        "mode": "SIMULATION"
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
