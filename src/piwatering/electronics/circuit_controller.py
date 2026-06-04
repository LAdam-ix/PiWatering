from db import write


class CircuitController:
    def __init__(self, name):
        self.name = name
        self.valves = []
        self.sensors = []

    def add_valve(self, valve):
        self.valves.append(valve)

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def activate_all_valves(self):
        for valve in self.valves:
            valve.open()

    def deactivate_all_valves(self):
        for valve in self.valves:
            valve.close()

    def get_sensors_html(self):
        return ''.join([sensor.get_html() for sensor in self.sensors])

    def get_valves_html(self):
        return ''.join([valve.get_html() for valve in self.valves])

    def get_html(self):
        sensors_html = self.get_sensors_html()
        valves_html = self.get_valves_html()
        return f'''
            <div class="circuit" id="{self.name}">
                <h1>{self.name}</h1>
                <div class="sensors">
                    {sensors_html}
                </div>
                <div class="valves">
                    {valves_html}
                </div>
            </div>
        '''

    def check_sensors(self):
        return {sensor.name: sensor.is_active() for sensor in self.sensors}

    def save_to_db(self):
        for sensor in self.sensors:
            write(
                "soil_moisture",
                {"circuit": self.name, "sensor": sensor.name},
                {"raw": float(sensor.read_raw_value()), "percent": float(sensor.read_value())},
            )
