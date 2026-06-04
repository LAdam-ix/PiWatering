import requests
from config import VM_URL

# VictoriaMetrics /write endpoint - one DB for the whole app
WRITE_URL = f"{VM_URL.rstrip('/')}/write"


def slug(text):
    """DB-safe label: replace line-protocol special chars (space, comma, equals)."""
    return str(text).replace(" ", "_").replace(",", ".").replace("=", "-")


def write(measurement, tags, fields, url=None):
    """Format one labeled sample as line protocol and POST it (single pass).

    Uses the global WRITE_URL unless `url` overrides it for a special case.
    Tag values are slugged, so no escaping is needed. No timestamp -> VM stamps
    receive-time. No buckets/org/token -> VM auto-creates the series.
    """
    tag_str = "".join(f",{k}={slug(v)}" for k, v in tags.items())
    field_str = ",".join(f"{k}={v}" for k, v in fields.items())
    line = f"{measurement}{tag_str} {field_str}"
    try:
        requests.post(url or WRITE_URL, data=line.encode(), timeout=2)
    except requests.RequestException as e:
        print(f"metrics write failed: {e}")
