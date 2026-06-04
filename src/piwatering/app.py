from config import FLASK_SECRET_KEY
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from electronics.valve import Valve
from electronics.garden_controller import GardenController
from electronics.pinout import VALVES

app = Flask(__name__, template_folder='./../../templates')
app.secret_key = FLASK_SECRET_KEY

# Web refresh interval in seconds
REFRESH_INTERVAL = 2

# Build the flat valve registry from the pinout dict
garden = GardenController(30)
for name, cfg in VALVES.items():
    garden.add_valve(Valve(name=name, role=cfg["role"], pin=cfg["pin"]))

garden.start_monitoring()


@app.route("/")
def index():
    return render_template("index.html", refresh_interval=REFRESH_INTERVAL, garden=garden)


@app.route("/valve/<name>/open", methods=["POST"])
def open_valve(name):
    v = garden.get_valve(name)
    if v:
        v.open()
        flash(f"{name} opened.")
    return redirect(url_for("index"))


@app.route("/valve/<name>/close", methods=["POST"])
def close_valve(name):
    v = garden.get_valve(name)
    if v:
        if v.timer_running:
            v.stop_timer()      # cancel the timer; its thread closes the valve
        else:
            v.close()
        flash(f"{name} closed.")
    return redirect(url_for("index"))


@app.route("/valve/<name>/timer", methods=["POST"])
def start_timer(name):
    v = garden.get_valve(name)
    if v:
        duration = request.form.get("duration", "")
        if not duration.isdigit():
            flash("Invalid duration.")
            return redirect(url_for("index"))
        v.start_timer(int(duration))
        flash(f"Timer started for {name}.")
    return redirect(url_for("index"))


@app.route("/valve/<name>/timer/stop", methods=["POST"])
def stop_timer(name):
    v = garden.get_valve(name)
    if v:
        v.stop_timer()
        flash(f"Timer stopped for {name}.")
    return redirect(url_for("index"))


@app.route("/valves/status", methods=["GET"])
def valves_status():
    return jsonify({
        v.name: {
            "open": v.is_open,
            "wired": v.wired,
            "role": v.role,
            "timer_remaining": v.timer_remaining,
        }
        for v in garden.valves
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
