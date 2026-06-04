

from config import FLASK_SECRET_KEY
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from electronics.valve import Valve
from electronics.circuit_controller import CircuitController
from electronics.garden_controller import GardenController
from electronics.sensor import Sensor
from electronics.pinout import RELAY1, RELAY2, RELAY7, CLOCK, MOSI, MISO, SELECT

app = Flask(__name__, template_folder='./../../templates')
app.secret_key = FLASK_SECRET_KEY
 
# Define the refresh interval in seconds
REFRESH_INTERVAL = 2

# Initialize GardenController and add circuits
garden_controller = GardenController(30)

# Initialize circuits
circuit1 = CircuitController(name="GRASS")
circuit2 = CircuitController(name="GARDEN")

# Add valves to circuits using the correct relay pins
circuit1.add_valve(Valve(name="Valve 1.1", pin=RELAY1))
circuit2.add_valve(Valve(name="Valve 2.1", pin=RELAY2))

# Add soil and rain sensors to circuits with MCP3008 configuration
soil_sensor_1 = Sensor(
    name="Soil Channel 0",
    channel=0,
    threshold=0.5,
    clock=CLOCK,
    mosi=MOSI,
    miso=MISO,
    select=SELECT,
)
soil_sensor_2 = Sensor(
    name="Soil Channel 1",
    channel=1,
    threshold=0.5,
    clock=CLOCK,
    mosi=MOSI,
    miso=MISO,
    select=SELECT,
)
circuit1.add_sensor(soil_sensor_1)
circuit1.add_sensor(soil_sensor_2)

soil_sensor_3 = Sensor(
    name="Soil Channel 2",
    channel=2,
    threshold=0.5,
    clock=CLOCK,
    mosi=MOSI,
    miso=MISO,
    select=SELECT,
)
soil_sensor_4 = Sensor(
    name="Soil Channel 3",
    channel=3,
    threshold=0.5,
    clock=CLOCK,
    mosi=MOSI,
    miso=MISO,
    select=SELECT,
)
circuit2.add_sensor(soil_sensor_3)
circuit2.add_sensor(soil_sensor_4)

# Add circuits to garden
garden_controller.add_circuit(circuit1)
garden_controller.add_circuit(circuit2)

# Optionally add main valve
main_valve = Valve(name="Main Valve", pin=RELAY7)
garden_controller.set_main_valve(main_valve)

garden_controller.start_monitoring()

@app.route("/")
def index():
    garden_controller.check_main_sensors()
    garden_html = garden_controller.get_html()
    return render_template(
        "index.html",
        garden_html=garden_html,
        refresh_interval=REFRESH_INTERVAL,
        garden_controller=garden_controller,
    )


@app.route("/main/activate_valve", methods=["POST"])
def activate_main_valve():
    garden_controller.get_main_valve().open()
    flash("Main valve activated.")
    return redirect(url_for("index"))


@app.route("/main/sensor_statuses", methods=["GET"])
def main_sensor_statuses():
    statuses = {}
    # statuses = garden_controller.check_main_sensors()
    return jsonify(statuses)

@app.route("/<circuit_name>/<valve_name>/open_valve", methods=["POST"])
def open_valve(circuit_name, valve_name):
    circuit = garden_controller.get_circuit_by_name(circuit_name)
    if circuit:
        valve = next((v for v in circuit.valves if v.name == valve_name), None)
        if valve:
            valve.open()
            flash(f"{valve_name} opened in {circuit_name}.")
    return redirect(url_for("index"))

@app.route("/<circuit_name>/<valve_name>/close_valve", methods=["POST"])
def close_valve(circuit_name, valve_name):
    circuit = garden_controller.get_circuit_by_name(circuit_name)
    if circuit:
        valve = next((v for v in circuit.valves if v.name == valve_name), None)
        if valve:
            valve.close()
            flash(f"{valve_name} closed in {circuit_name}.")
    return redirect(url_for("index"))


@app.route("/<circuit_name>/<valve_name>/start_timer", methods=["POST"])
def start_timer(circuit_name, valve_name):
    circuit = garden_controller.get_circuit_by_name(circuit_name)
    if circuit:
        valve = next((v for v in circuit.valves if v.name == valve_name), None)
        if valve:
            duration_seconds = request.form.get("duration")
            if not duration_seconds.isdigit():
                flash("Invalid duration input.")
                return redirect(url_for("index"))
            valve.start_timer(int(duration_seconds))
            flash(f"Timer started for {valve_name} in {circuit_name}.")
    return redirect(url_for("index"))



@app.route("/<circuit_name>/sensor_statuses", methods=["GET"])
def sensor_statuses(circuit_name):
    circuit = garden_controller.get_circuit_by_name(circuit_name)
    if circuit:
        statuses = {}
        for sensor in circuit.sensors:
            statuses[sensor.name.replace(" ", "_")] = {
                "active": sensor.is_active(),
                "raw_value": sensor.read_raw_value(),
                "h_value": sensor.read_value(),
            }
        return jsonify(statuses)
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
