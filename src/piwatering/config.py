from dotenv import dotenv_values

config = dotenv_values(".env")

SENSOR_MIN = float(config.get("SENSOR_MIN", 0.6)) 
SENSOR_MAX = float(config.get("SENSOR_MAX", 0.2))

INFLUX_URL = config.get("INFLUX_URL", "http://localhost:8086")
INFLUX_ORG = config.get("INFLUX_ORG", "Default")
INFLUX_TOKEN = config.get("INFLUX_TOKEN", "")
