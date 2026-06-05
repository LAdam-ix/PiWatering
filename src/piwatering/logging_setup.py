import logging

from config import LOG_LEVEL, LOG_FILE, ACCESS_LOG

# Paths the frontend polls frequently (background "internal" traffic) - their
# access-log lines are the spam we want to drop by default.
POLL_PATHS = ("/valves/status",)


class _SkipPolling(logging.Filter):
    """Drop access-log lines for the frequent frontend poll; keep real requests."""

    def filter(self, record):
        msg = record.getMessage()
        return not any(p in msg for p in POLL_PATHS)


def setup_logging():
    """Configure the app logger ('piwater'): clear [piwater] prefix, optional
    file output (LOG_FILE). Werkzeug access log keeps real requests but drops the
    frequent poll unless ACCESS_LOG=true (then everything is logged)."""
    fmt = logging.Formatter("%(asctime)s [piwater] %(levelname)s %(message)s", "%H:%M:%S")

    log = logging.getLogger("piwater")
    log.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    log.handlers.clear()
    log.propagate = False

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    log.addHandler(console)

    if LOG_FILE:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(fmt)
        log.addHandler(file_handler)

    # Werkzeug per-request HTTP log: keep real requests, drop the poll unless asked
    wlog = logging.getLogger("werkzeug")
    wlog.setLevel(logging.INFO)
    wlog.filters.clear()
    if not ACCESS_LOG:
        wlog.addFilter(_SkipPolling())

    return log
