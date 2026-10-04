# src/feedback.py
import time
import pyttsx3
from collections import defaultdict
from config import (
    THRESHOLD_SAFE, THRESHOLD_WARNING, THRESHOLD_DANGER,
    COOLDOWN_SECONDS, SPEAK_RATE
)

class FeedbackSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', SPEAK_RATE)
        self.last_speak = defaultdict(float)

    def get_vibration_level(self, distance_cm):
        if distance_cm > THRESHOLD_SAFE:
            return 0, "sin vibración"
        elif distance_cm > THRESHOLD_WARNING:
            return 1, "vibración SUAVE (75-100 cm)"
        elif distance_cm > THRESHOLD_DANGER:
            return 2, "vibración MEDIA (40-75 cm)"
        else:
            return 3, "vibración FUERTE (<40 cm)"

    def speak(self, text, key="general"):
        now = time.time()
        if now - self.last_speak[key] > COOLDOWN_SECONDS:
            print(f"\n🔊 AUDIO: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            self.last_speak[key] = now

    def notify(self, detections):
        if not detections:
            return

        closest = detections[0]
        dist = closest["distance_cm"]
        name = closest["name"]
        level, desc = self.get_vibration_level(dist)

        if level > 0:
            intensity = "█" * level + "░" * (3 - level)
            print(f"📳 VIBRACIÓN [{intensity}] → {desc} | Objeto: {name} a {dist} cm")

        if dist < THRESHOLD_DANGER:
            self.speak(f"¡Cuidado! {name} muy cerca, a {dist} centímetros", key="danger")
        elif dist < THRESHOLD_WARNING:
            self.speak(f"{name} a {dist} centímetros", key="warning")

