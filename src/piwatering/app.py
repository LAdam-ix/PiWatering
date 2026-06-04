from config import FLASK_SECRET_KEY
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from electronics.valve import Valve
from electronics.watering_controller import WateringController
from electronics.pinout import VALVES

app = Flask(__name__, template_folder='./../../templates')
app.secret_key = FLASK_SECRET_KEY

# Web refresh interval in seconds
REFRESH_INTERVAL = 2

# Build the flat valve registry from the pinout dict (key = stable id)
controller = WateringController(30)
for vid, cfg in VALVES.items():
    controller.add_valve(Valve(id=vid, label=cfg["label"], role=cfg["role"], pin=cfg["pin"]))

controller.start_monitoring()


@app.route("/")
def index():
    return render_template("index.html", refresh_interval=REFRESH_INTERVAL, controller=controller)


@app.route("/valve/<valve_id>/open", methods=["POST"])
def open_valve(valve_id):
    v = controller.get_valve(valve_id)
    if v:
        v.open()
        flash(f"{v.label} opened.")
    return redirect(url_for("index"))


@app.route("/valve/<valve_id>/close", methods=["POST"])
def close_valve(valve_id):
    v = controller.get_valve(valve_id)
    if v:
        if v.timer_running:
            v.stop_timer()      # cancel the timer; its thread closes the valve
        else:
            v.close()
        flash(f"{v.label} closed.")
    return redirect(url_for("index"))


@app.route("/valve/<valve_id>/timer", methods=["POST"])
def start_timer(valve_id):
    v = controller.get_valve(valve_id)
    if v:
        duration = request.form.get("duration", "")
        if not duration.isdigit():
            flash("Invalid duration.")
            return redirect(url_for("index"))
        v.start_timer(int(duration))
        flash(f"Timer started for {v.label}.")
    return redirect(url_for("index"))


@app.route("/valve/<valve_id>/timer/stop", methods=["POST"])
def stop_timer(valve_id):
    v = controller.get_valve(valve_id)
    if v:
        v.stop_timer()
        flash(f"Timer stopped for {v.label}.")
    return redirect(url_for("index"))


@app.route("/valves/status", methods=["GET"])
def valves_status():
    return jsonify({
        v.id: {
            "label": v.label,
            "open": v.is_open,
            "wired": v.wired,
            "role": v.role,
            "timer_remaining": v.timer_remaining,
        }
        for v in controller.valves
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
