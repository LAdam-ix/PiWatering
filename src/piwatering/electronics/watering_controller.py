import threading
import time

from db import write


class WateringController:
    def __init__(self, log_interval=60):
        self.valves = []
        self.sensors = []           # flat; planned/inactive for now
        self._log_interval = log_interval
        self._monitor_thread = None

    def add_valve(self, valve):
        self.valves.append(valve)

    def get_valve(self, valve_id):
        for v in self.valves:
            if v.id == valve_id:
                return v
        return None

    def zones(self):
        return [v for v in self.valves if v.role == "zone"]

    def sources(self):
        return [v for v in self.valves if v.role == "source"]

    def deactivate_all_valves(self):
        for v in self.valves:
            v.close()

    def start_monitoring(self, log_interval=None):
        interval = self._log_interval if log_interval is None else log_interval
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,), daemon=True
        )
        self._monitor_thread.start()

    def _monitor_loop(self, interval):
        while True:
            for s in self.sensors:
                write(
                    "soil_moisture",
                    {"zone": getattr(s, "zone", ""), "sensor": s.name},
                    {"raw": float(s.read_raw_value()), "percent": float(s.read_value())},
                )
            time.sleep(interval)
