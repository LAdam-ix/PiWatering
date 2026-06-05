from dotenv import dotenv_values

config = dotenv_values(".env")

# Soil-moisture calibration (raw MCP3008 value 0..1, inverted: wet < dry)
SENSOR_RAW_WET = float(config.get("SENSOR_RAW_WET", 0.2))  # -> 100 %
SENSOR_RAW_DRY = float(config.get("SENSOR_RAW_DRY", 0.6))  # ->   0 %

# VictoriaMetrics (InfluxDB line-protocol /write endpoint)
VM_URL = config.get("VM_URL", "http://localhost:8428")

FLASK_SECRET_KEY = config.get("FLASK_SECRET_KEY", "change-me-in-env")
FLASK_PORT = int(config.get("FLASK_PORT", 5000))

# Logging
LOG_LEVEL = config.get("LOG_LEVEL", "INFO")        # DEBUG / INFO / WARNING / ...
LOG_FILE = config.get("LOG_FILE", "")              # empty = console (journal) only
ACCESS_LOG = config.get("ACCESS_LOG", "false").lower() in ("1", "true", "yes")  # Werkzeug HTTP log
