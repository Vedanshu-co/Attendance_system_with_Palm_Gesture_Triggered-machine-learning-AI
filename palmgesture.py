import sys
import os
import time
import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime

# ===================== PATH SETUP =====================
BASE_DIR = "faces"
CROPPED_DIR = os.path.join(BASE_DIR, "cropped")
FULL_DIR = os.path.join(BASE_DIR, "full")

os.makedirs(CROPPED_DIR, exist_ok=True)
os.makedirs(FULL_DIR, exist_ok=True)

# ===================== MODELS =====================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ===================== MJPEG STREAM READER =====================
def mjpeg_stream():
    buffer = b""
    for chunk in sys.stdin.buffer:
        buffer += chunk
        start = buffer.find(b'\xff\xd8')  # JPEG start
        end = buffer.find(b'\xff\xd9')    # JPEG end
        if start != -1 and end != -1:
            jpg = buffer[start:end + 2]
            buffer = buffer[end + 2:]
            frame = cv2.imdecode(
                np.frombuffer(jpg, dtype=np.uint8),
                cv2.IMREAD_COLOR
            )
            if frame is not None:
                yield frame

# ===================== VARIABLES =====================
COUNTDOWN_TIME = 5
countdown_started = False
start_time = None
capture_done = False

print("[INFO] Palm gesture system started (libcamera MJPEG mode)")
print("[INFO] Waiting for camera stream...")

# ===================== MAIN LOOP =====================
for frame in mjpeg_stream():

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # ---------- PALM DETECTION ----------
    if results.multi_hand_landmarks and not capture_done:
        if not countdown_started:
            start_time = time.time()
            countdown_started = True
            print("[INFO] Palm detected, countdown started")

    # ---------- COUNTDOWN ----------
    if countdown_started and not capture_done:
        elapsed = int(time.time() - start_time)
        remaining = COUNTDOWN_TIME - elapsed

        if remaining <= 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                print("[WARN] No faces detected, retrying...")
                countdown_started = False
                start_time = None
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # ---------- SAVE FULL IMAGE ----------
            full_path = os.path.join(FULL_DIR, f"full_{timestamp}.jpg")
            cv2.imwrite(full_path, frame)
            print(f"[INFO] Full image saved: {full_path}")

            # ---------- SAVE ALL CROPPED FACES ----------
            for idx, (x, y, w, h) in enumerate(faces, start=1):
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (200, 200))

                cropped_path = os.path.join(
                    CROPPED_DIR, f"face_{timestamp}_{idx}.jpg"
                )
                cv2.imwrite(cropped_path, face_img)
                print(f"[INFO] Cropped face {idx} saved: {cropped_path}")

            print(f"[INFO] Capture completed ({len(faces)} faces)")
            capture_done = True

    time.sleep(0.005)

print("[INFO] Palm capture program ended")
