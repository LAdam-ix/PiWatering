from gpiozero import OutputDevice
import time
from threading import Thread
from influxdb_client import Point,WritePrecision

class Valve(OutputDevice):
    def __init__(self, name, pin, db_api=None, active_high=False, initial_value=False):
        super().__init__(pin, active_high=active_high, initial_value=initial_value)
        self.name = name
        self.timer_running = False
        self.db_api = db_api

    def open(self):
        if self.db_api:
            point_open = Point("valve_status") \
                .tag("valve_id", self.name) \
                .field("state", 1) \
                .time(time.time_ns(),WritePrecision.NS)
            try:
                self.db_api.write(record=point_open, bucket="Valves")
            except Exception as e:
                print(f"Error writing to InfluxDB: {e}")
        print(f'{self.name} opened')
        self.on()

    def close(self):
        if self.db_api:
            point_close = Point("valve_status") \
                .tag("valve_id", self.name) \
                .field("state", 0) \
               .time(time.time_ns(), WritePrecision.NS)
            try:
                self.db_api.write(record=point_close, bucket="Valves") 
            except Exception as e:
                print(f"Error writing to InfluxDB: {e}")
        print(f'{self.name} closed')
        self.off()

    def start_timer(self, duration_seconds):
        if not self.timer_running:
            timer_thread = Thread(target=self._timer_function, args=(duration_seconds,))
            timer_thread.start()

    def _timer_function(self, duration_seconds):
        self.timer_running = True
        self.open()
        time.sleep(duration_seconds)
        self.close()
        self.timer_running = False

    def get_html(self):
        return f'''
        <div id="{self.name}">
            <h2>{self.name}</h2>
            <form action="/{self.name}/open_valve" method="post">
                <button type="submit">Open Valve</button>
            </form>
            <form action="/{self.name}/close_valve" method="post">
                <button type="submit">Close Valve</button>
            </form>
            <form action="/{self.name}/start_timer" method="post">
                <label for="{self.name}_duration">Timer Duration (seconds):</label>
                <input type="number" id="{self.name}_duration" name="duration" required>
                <button type="submit">Start Timer</button>
            </form>
            <hr>
        </div>
    '''
