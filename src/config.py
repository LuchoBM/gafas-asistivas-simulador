# src/config.py

# ========== CÁMARA DEL TELÉFONO ==========
# Cambia esta URL por la que te da la app IP Webcam
CAMERA_URL = "http://192.168.227.175:8080/video"   # <-- CAMBIA ESTO

# ========== UMBRALES DE DISTANCIA (cm simulados) ==========
THRESHOLD_SAFE = 100      # > 100 cm → sin vibración
THRESHOLD_WARNING = 75    # 75-100 cm → vibración suave
THRESHOLD_DANGER = 40     # 40-75 cm → media
THRESHOLD_CRITICAL = 20   # < 20 cm → fuerte

# ========== YOLO ==========
MODEL_PATH = "yolov8n.pt"   # se descarga solo la primera vez
CONFIDENCE = 0.45

# Clases prioritarias
PRIORITY_CLASSES = {
    "person", "car", "truck", "bus", "motorcycle", "bicycle",
    "traffic light", "stop sign", "bench", "chair", "dog", "cat"
}

# ========== FEEDBACK ==========
COOLDOWN_SECONDS = 2.5
SPEAK_RATE = 160
