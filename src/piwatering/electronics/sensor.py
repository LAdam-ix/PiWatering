from config import SENSOR_RAW_WET, SENSOR_RAW_DRY
from gpiozero import MCP3008

# Raw value the ADC returns when the probe is disconnected/off -> report 0 %
SENSOR_DISCONNECTED_RAW = 0.000489


class Sensor:
    def __init__(self, name, channel, threshold, clock, mosi, miso, select):
        self.name = name
        self.sensor = MCP3008(channel=channel, clock_pin=clock, mosi_pin=mosi, miso_pin=miso, select_pin=select)
        self.threshold = threshold

    def read_raw_value(self):
        return self.sensor.value

    def read_value(self):
        if round(self.sensor.value, 6) == SENSOR_DISCONNECTED_RAW:
            return 0
        return 100 - (self.sensor.value - SENSOR_RAW_WET) * 100 / (SENSOR_RAW_DRY - SENSOR_RAW_WET)

    def is_active(self):
        return self.read_value() > self.threshold

    def get_html(self):
        return f'<p>{self.name}: <span id="{self.name}_status">Unknown</span>, Value: <span id="{self.name}_value"></span></p>'
