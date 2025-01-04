import time
from influxdb_client import Point, WritePrecision, WriteOptions

class CircuitController:
    def __init__(self, name, database):
        self.name = name
        self.valves = []
        self.sensors = []
        self.db_api = database

    def add_valve(self, valve):
        self.valves.append(valve)

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def activate_all_valves(self):
        for valve in self.valves:
            valve.activate_valve()

    def deactivate_all_valves(self):
        for valve in self.valves:
            valve.valve.off()

    def get_sensors_html(self):
        sensors_html = ''.join([sensor.get_html() for sensor in self.sensors])
        return sensors_html

    def get_valves_html(self):
        valve_html = ''.join([valve.get_html() for valve in self.valves])
        return valve_html

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
        sensor_statuses = {}
        for sensor in self.sensors:
            sensor_statuses[sensor.name] = sensor.is_active()
        return sensor_statuses


    def save_to_db(self):
        for sensor in self.sensors:
            raw_value = float(sensor.read_raw_value())
            value = float(sensor.read_value())
            cur_time = time.time_ns() 
            point1 = Point("sensor") \
                .tag("sensor", sensor.name) \
                .field("value", raw_value) \
                .time(cur_time, WritePrecision.NS)
            point2 = Point("sensor") \
                .tag("sensor", sensor.name) \
                .field("value", value) \
                .time(cur_time, WritePrecision.NS)
            self.db_api.write(bucket=f"{self.name}_raw_sensors", record=point1)
            self.db_api.write(bucket=f"{self.name}_h_sensors",  record=point2)
