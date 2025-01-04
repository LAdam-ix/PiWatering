import threading
import time


class GardenController:
    def __init__(self):
        self.circuits = []
        ## for futere sensors that will monitor 
        ## if it's raining and the level of the water in the tank
        self.special_sensors = []
        self.main_valve = None
        self.monitoring = None

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def add_special_sensor(self, sensor):
        self.special_sensors.append(sensor)

    def set_main_valve(self, valve):
        self.main_valve = valve

    def deactivate_all_valves(self):
        if self.main_valve:
            self.main_valve.valve.off()
        for circuit in self.circuits:
            circuit.deactivate_all_valves()

    def check_special_sensors(self):
        for sensor in self.special_sensors:
            if sensor.is_pressed:
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
    
    def start_monitoring(self, log_interval=60):
        self.monitoring = threading.Thread(target=self._start_monitoring, args=(log_interval,))
        self.monitoring.start()

    def _start_monitoring(self, time_interval=60):
        while True:
            for circuit in self.circuits:
                circuit.save_to_db()
            time.sleep(time_interval)