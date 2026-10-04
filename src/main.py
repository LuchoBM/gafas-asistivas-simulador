# src/main.py
import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CAMERA_URL
from detector import ObstacleDetector
from feedback import FeedbackSystem

def main():
    print("=" * 60)
    print("  SIMULADOR DE GAFAS ASISTIVAS - Prototipo Mediano Plazo")
    print("=" * 60)
    print(f"Conectando a cámara: {CAMERA_URL}")
    print("Presiona 'q' para salir")
    print("-" * 60)

    detector = ObstacleDetector()
    feedback = FeedbackSystem()

    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        print("\n❌ ERROR: No se pudo abrir el stream de la cámara.")
        print("1. Abre la app IP Webcam en el teléfono")
        print("2. Inicia el servidor")
        print("3. Copia la URL (ej: http://192.168.x.x:8080/video)")
        print("4. Pégala en src/config.py → CAMERA_URL")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        detections, results = detector.process(frame)
        feedback.notify(detections)

        annotated = results.plot()
        cv2.putText(annotated, "SIMULADOR GAFAS ASISTIVAS", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Simulador - Vista de las gafas", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nSimulador cerrado.")

if __name__ == "__main__":
    main()
