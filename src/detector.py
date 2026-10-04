# src/detector.py
from ultralytics import YOLO
import numpy as np
from config import MODEL_PATH, CONFIDENCE, PRIORITY_CLASSES

class ObstacleDetector:
    def __init__(self):
        print("Cargando modelo YOLO... (puede tardar la primera vez)")
        self.model = YOLO(MODEL_PATH)
        print("Modelo listo.")

    def estimate_distance(self, box, frame_height):
        """Simula distancia en cm según el tamaño del bounding box"""
        x1, y1, x2, y2 = box
        height_ratio = (y2 - y1) / frame_height

        if height_ratio > 0.55:
            return 15
        elif height_ratio > 0.40:
            return 30
        elif height_ratio > 0.28:
            return 50
        elif height_ratio > 0.18:
            return 75
        elif height_ratio > 0.10:
            return 120
        else:
            return 200

    def process(self, frame):
        results = self.model(frame, conf=CONFIDENCE, verbose=False, device="cpu")[0]
        h, w = frame.shape[:2]

        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            name = self.model.names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy()

            if name in PRIORITY_CLASSES:
                dist_cm = self.estimate_distance(xyxy, h)
                detections.append({
                    "name": name,
                    "confidence": conf,
                    "distance_cm": dist_cm,
                    "box": xyxy
                })

        detections.sort(key=lambda x: x["distance_cm"])
        return detections, results

