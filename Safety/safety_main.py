import asyncio
from safety.watchdog import Watchdog
from safety.fault_detection import FaultDetection
from safety.safe_shutdown import SafeShutdown

async def main_loop():
    wd = Watchdog(timeout_s=1.0)
    fd = FaultDetection()
    ss = SafeShutdown()

    sensors = {"imu": 0.0, "fsr": 0.0, "temp": 25.0}
    actuators = {"servo1": 0, "servo2": 0, "max_limit": 180}
    power = {"v_batt": 24.0, "max_voltage": 24.0}

    def wd_callback():
        print("Watchdog timeout! Executing safe shutdown.")
        asyncio.run(ss.execute_shutdown(actuators, power))

    wd.start_monitor(wd_callback)

    while True:
        wd.heartbeat()
        faults = await fd.check_faults(sensors, actuators, power)
        if faults:
            print("Detected faults:", faults)
            await ss.execute_shutdown(actuators, power)
            break
        actuators["servo1"] += 1
        actuators["servo2"] += 1
        await asyncio.sleep(0.05)

if __name__ == "__main__":
    asyncio.run(main_loop())
