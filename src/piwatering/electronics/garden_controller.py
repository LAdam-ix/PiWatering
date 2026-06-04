import threading
import time


class GardenController:
    def __init__(self, log_interval=60):
        self.circuits = []
        self.main_sensors = []      # garden-level sensors (e.g. water-level) - planned
        self.main_valve = None      # special master shutoff (normally open)
        self._log_interval = log_interval
        self._monitor_thread = None

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def add_main_sensor(self, sensor):
        self.main_sensors.append(sensor)

    def set_main_valve(self, valve):
        self.main_valve = valve

    def deactivate_all_valves(self):
        if self.main_valve:
            self.main_valve.close()
        for circuit in self.circuits:
            circuit.deactivate_all_valves()

    def check_main_sensors(self):
        # Emergency shutoff: if any garden-level sensor is active, stop all water
        for sensor in self.main_sensors:
            if sensor.is_active():
                self.deactivate_all_valves()
                break

    def get_html(self):
        circuit_html = ''.join([circuit.get_html() for circuit in self.circuits])
        main_valve_html = self.main_valve.get_html() if self.main_valve else ''
        return main_valve_html + circuit_html

    def get_circuit_by_name(self, name):
        for circuit in self.circuits:
            if circuit.name == name:
                return circuit
        return None

    def get_main_valve(self):
        return self.main_valve

    def start_monitoring(self, log_interval=None):
        interval = self._log_interval if log_interval is None else log_interval
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,), daemon=True
        )
        self._monitor_thread.start()

    def _monitor_loop(self, time_interval):
        while True:
            for circuit in self.circuits:
                circuit.save_to_db()
            time.sleep(time_interval)
