import math
import time

def compute_heading(mag):
    """
    mag: (mx, my, mz)
    return heading in degrees(0–360)
    """
    mx, my, _ = mag

    heading_rad = math.atan2(my, mx)
    heading_deg = math.degrees(heading_rad)

    if heading_deg < 0:
        heading_deg += 360

    return heading_deg


# (GPS-based)
class VelocityEstimator:
    def __init__(self):
        self.prev_lat = None
        self.prev_lon = None
        self.prev_time = None

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius (m)
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def update(self, gps):
        if gps["lat"] is None:
            return 0.0

        current_time = time.time()

        if self.prev_lat is None:
            self.prev_lat = gps["lat"]
            self.prev_lon = gps["lon"]
            self.prev_time = current_time
            return 0.0

        distance = self.haversine(
            self.prev_lat, self.prev_lon,
            gps["lat"], gps["lon"]
        )

        dt = current_time - self.prev_time
        velocity = distance / dt if dt > 0 else 0.0

        self.prev_lat = gps["lat"]
        self.prev_lon = gps["lon"]
        self.prev_time = current_time

        return velocity# m/s
