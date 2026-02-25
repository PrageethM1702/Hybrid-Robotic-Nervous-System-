import cv2
from visionNN.obstacledetector import ObstacleDetector
from visionNN.terrain_classifier import TerrainClassifier

class VisionNN:
    def __init__(self, obstacle_model_path="yolov8n.pt", terrain_device=None, obstacle_conf=0.4):
        self.obstacle_detector = ObstacleDetector(model_path=obstacle_model_path, conf_threshold=obstacle_conf)
        self.terrain_classifier = TerrainClassifier(device=terrain_device)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        terrain_info = self.terrain_classifier.predict(rgb_frame)
        obstacles = self.obstacle_detector.detect(rgb_frame)
        return {
            "terrain": terrain_info,
            "obstacles": obstacles
        }

if __name__ == "__main__":
    stream_url = "http://************8"
    cap = cv2.VideoCapture(stream_url)

    vision = VisionNN()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from Pi stream")
            break

        output = vision.process_frame(frame)
        print("Terrain:", output["terrain"])
        print("Obstacles:", output["obstacles"])

        cv2.imshow("HRNS-Q Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
