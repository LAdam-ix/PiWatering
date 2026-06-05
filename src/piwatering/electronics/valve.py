import logging
import time
from threading import Thread, Event

from gpiozero import OutputDevice

from db import write

log = logging.getLogger("piwater")


class Valve:
    """A relay-driven valve. `pin=None` => not wired yet (logged, no GPIO)."""

    def __init__(self, id, label, role="zone", pin=None, active_high=False, initial_value=False):
        self.id = id
        self.label = label
        self.role = role
        self.timer_running = False
        self.timer_paused = False
        self.timer_seconds = None       # total duration of the current timer
        self._remaining = 0             # authoritative seconds left (used while paused)
        self._ends_at = None            # monotonic end time while actively counting
        self._event = Event()           # interrupts the countdown wait (pause/resume/stop)
        self._stopping = False
        # Logical open/closed (commanded) state, starts closed. Independent of the
        # relay's electrical default - the relay->valve mapping (NO/NC contact,
        # active_high) is a separate physical concern, configurable per valve later.
        self._open = False
        self._device = (
            OutputDevice(pin, active_high=active_high, initial_value=initial_value)
            if pin is not None else None
        )

    @property
    def wired(self):
        return self._device is not None

    @property
    def is_open(self):
        return self._open

    @property
    def timer_remaining(self):
        if not self.timer_running:
            return 0
        if self.timer_paused or self._ends_at is None:
            return self._remaining
        return max(0, round(self._ends_at - time.monotonic()))

    def open(self):
        self._open = True
        write("valve_state", {"valve": self.id}, {"value": 1})
        if self._device:
            self._device.on()
        log.info("%s opened", self.id)

    def close(self):
        self._open = False
        write("valve_state", {"valve": self.id}, {"value": 0})
        if self._device:
            self._device.off()
        log.info("%s closed", self.id)

    # ---- timer (start / pause / resume / stop) ----
    def start_timer(self, duration_seconds):
        if self.timer_running:
            return
        self.timer_running = True
        self.timer_paused = False
        self._stopping = False
        self.timer_seconds = duration_seconds
        self._remaining = duration_seconds
        self._event.clear()
        Thread(target=self._run_timer, daemon=True).start()

    def pause_timer(self):
        if self.timer_running and not self.timer_paused:
            self.timer_paused = True
            self._event.set()

    def resume_timer(self):
        if self.timer_running and self.timer_paused:
            self.timer_paused = False
            self._event.set()

    def stop_timer(self):
        if self.timer_running:
            self._stopping = True
            self._event.set()

    def _run_timer(self):
        self.open()
        while self._remaining > 0 and not self._stopping:
            self._event.clear()
            if self.timer_paused:
                self.close()                 # pause closes the valve, keeps remaining
                self._event.wait()           # sleep until resume or stop
                if self._stopping:
                    break
                self.open()                  # resumed
                continue
            self._ends_at = time.monotonic() + self._remaining
            interrupted = self._event.wait(self._remaining)
            self._remaining = max(0, round(self._ends_at - time.monotonic()))
            if not interrupted:
                self._remaining = 0          # ran to completion
        self.close()
        self.timer_running = False
        self.timer_paused = False
        self._ends_at = None
        self._remaining = 0
