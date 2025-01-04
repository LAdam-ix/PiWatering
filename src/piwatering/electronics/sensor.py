from src.piwatering.config import SENSOR_MAX, SENSOR_MIN
from gpiozero import MCP3008

class Sensor:
    def __init__(self, name, channel, threshold, clock, mosi, miso, select):
        self.name = name
        self.sensor = MCP3008(channel=channel, clock_pin=clock, mosi_pin=mosi, miso_pin=miso, select_pin=select)
        self.threshold = threshold

    def read_raw_value(self):
        return self.sensor.value
    
    def read_value(self):
        ## this is value when the sensor pin is unused(gronded)
        if 0.000489 == round(self.sensor.value, 6):
            return 0
        
        return (self.sensor.value - SENSOR_MAX) * (-100) / (SENSOR_MIN - SENSOR_MAX)


    def is_active(self):
        return self.read_value() > self.threshold

    def get_html(self):
        return f'<p>{self.name}: <span id="{self.name}_status">Unknown</span>, Value: <span id="{self.name}_value"></span></p>'
