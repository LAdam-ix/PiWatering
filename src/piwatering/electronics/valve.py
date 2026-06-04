import time
from threading import Thread, Event

from gpiozero import OutputDevice

from db import write


class Valve:
    """A relay-driven valve. `pin=None` => not wired yet (logged, no GPIO)."""

    def __init__(self, name, role="zone", pin=None, active_high=False, initial_value=False):
        self.name = name
        self.role = role
        self.timer_running = False
        self.timer_seconds = None       # total duration of the current timer
        self._timer_ends_at = None      # monotonic clock value when it will close
        self._timer_stop = Event()
        self._device = (
            OutputDevice(pin, active_high=active_high, initial_value=initial_value)
            if pin is not None else None
        )

    @property
    def wired(self):
        return self._device is not None

    @property
    def is_open(self):
        return bool(self._device and self._device.value)

    @property
    def timer_remaining(self):
        """Seconds left on the running timer (0 if none)."""
        if not self.timer_running or self._timer_ends_at is None:
            return 0
        return max(0, round(self._timer_ends_at - time.monotonic()))

    def open(self):
        write("valve_state", {"valve": self.name}, {"value": 1})
        if self._device:
            self._device.on()
        print(f"{self.name} opened")

    def close(self):
        write("valve_state", {"valve": self.name}, {"value": 0})
        if self._device:
            self._device.off()
        print(f"{self.name} closed")

    def start_timer(self, duration_seconds):
        if self.timer_running:
            return
        self.timer_running = True
        self.timer_seconds = duration_seconds
        self._timer_ends_at = time.monotonic() + duration_seconds
        self._timer_stop.clear()
        Thread(target=self._timer_function, args=(duration_seconds,), daemon=True).start()

    def stop_timer(self):
        """Cancel a running timer early; the timer thread then closes the valve."""
        self._timer_stop.set()

    def _timer_function(self, duration_seconds):
        self.open()
        self._timer_stop.wait(duration_seconds)   # wakes early if stop_timer() fired
        self.close()
        self.timer_running = False
        self.timer_seconds = None
        self._timer_ends_at = None
