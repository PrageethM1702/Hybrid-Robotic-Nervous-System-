import torch

class ObstacleDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.4):
        self.model = torch.hub.load('ultralytics/yolov8', 'custom', path=model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = det.tolist()
            if conf < self.conf_threshold:
                continue
            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": conf,
                "class": int(cls)
            })
        return detections
