RELAY1 = 3
RELAY2 = 2
RELAY3 = None
RELAY4 = None
RELAY5 = None
RELAY6 = None
RELAY7 = 4
RELAY8 = None

RED_TEST_LED = 19
BLUE_TEST_LED = 21

CLOCK=11
MOSI=10
MISO=9
SELECT=8

# 8-relay board. Valve registry: name -> {pin, role}.
#   pin  = relay channel BCM pin, or None until wired (None = present but not operable)
#   role = "source" (water input: mains/reservoir, act as masters) | "zone" (output)
VALVES = {
    "Town mains":   {"pin": None, "role": "source"},
    "Reservoir":    {"pin": None, "role": "source"},
    "Garden 1":     {"pin": None, "role": "zone"},
    "Garden 2":     {"pin": None, "role": "zone"},
    "Upper garden": {"pin": None, "role": "zone"},
    "Trees":        {"pin": None, "role": "zone"},
    "Hose":         {"pin": None, "role": "zone"},
    "Grass":        {"pin": None, "role": "zone"},
}
