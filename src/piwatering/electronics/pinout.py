## Number = GPIO Number 
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

# 8-relay board. Valve registry keyed by a STABLE id (never change it - used for
# routes, DB labels, lookups). `label` is the display name (freely changeable).
#   relay = which relay channel (its BCM pin, e.g. RELAY1), or None until wired
#   role = "source" (water input: mains/reservoir, act as masters) | "zone" (output)
VALVES = {
    "town_mains":   {"relay": None, "role": "source", "label": "Town mains"},
    "reservoir":    {"relay": None, "role": "source", "label": "Reservoir"},
    "garden_1":     {"relay": None, "role": "zone",   "label": "Garden 1"},
    "garden_2":     {"relay": None, "role": "zone",   "label": "Garden 2"},
    "upper_garden": {"relay": None, "role": "zone",   "label": "Upper garden"},
    "trees":        {"relay": None, "role": "zone",   "label": "Trees"},
    "hose":         {"relay": None, "role": "zone",   "label": "Hose"},
    "grass":        {"relay": None, "role": "zone",   "label": "Grass"},
}
