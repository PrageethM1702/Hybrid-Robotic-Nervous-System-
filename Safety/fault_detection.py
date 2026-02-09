import random
import asyncio

class FaultDetection:
    def __init__(self):
        self.active_faults = []

    async def check_faults(self, sensors, actuators, power):
        self.active_faults.clear()
        for name, val in sensors.items():
            if val is None or not isinstance(val, (int, float)):
                self.active_faults.append(f"Sensor fault: {name}")
        for name, val in actuators.items():
            if val > actuators.get("max_limit", 100):
                self.active_faults.append(f"Actuator overload: {name}")
        for name, val in power.items():
            if val < 0 or val > power.get("max_voltage", 24):
                self.active_faults.append(f"Power fault: {name}")
        if random.random() < 0.001:
            self.active_faults.append("Random system anomaly")
        return self.active_faults
