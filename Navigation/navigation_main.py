import time

from imu_gy801 import imu_init, get_imu_data
from gps_neo_m8n import get_gps_data
from nav_estimation import compute_heading, VelocityEstimator

def main():
    imu_init()
    vel_estimator = VelocityEstimator()

    print("HRNS-Q Navigation System Started")

    while True:
        imu = get_imu_data()
        gps = get_gps_data()

        heading = compute_heading(imu["mag"])
        velocity = vel_estimator.update(gps)

        print("------ HRNS-Q NAV DATA ------")
        print(f"Heading   : {heading:.2f} deg")
        print(f"Velocity  : {velocity:.2f} m/s")
        print(f"Accel     : {imu['accel']}")
        print(f"Gyro      : {imu['gyro']}")
        print(f"GPS       : {gps}")
        print("-----------------------------\n")

        time.sleep(0.2)

if __name__ == "__main__":
    main()
