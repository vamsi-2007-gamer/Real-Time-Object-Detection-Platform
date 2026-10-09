import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_name="yolo11n.pt"):
        self.model = YOLO(model_name)

    def detect(self, image_bgr, confidence=0.35):
        results = self.model.predict(source=image_bgr, conf=confidence, verbose=False)
        result = results[0]
        annotated = result.plot()
        detections = []
        if result.boxes is not None:
            names = result.names
            for box in result.boxes:
                coords = box.xyxy[0].tolist()
                class_id = int(box.cls[0].item())
                detections.append({
                    "label": str(names[class_id]),
                    "confidence": float(box.conf[0].item()),
                    "x1": int(coords[0]), "y1": int(coords[1]),
                    "x2": int(coords[2]), "y2": int(coords[3])
                })
        return cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), detections
