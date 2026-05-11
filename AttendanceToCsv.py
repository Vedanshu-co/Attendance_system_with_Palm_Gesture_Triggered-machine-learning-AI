import cv2
import os
import csv
from datetime import datetime

# ===================== PATH CONFIG =====================

CROPPED_FACE_DIR = "faces/cropped"
MODEL_PATH = "models/face_model.yml"
LABELS_PATH = "models/labels.txt"
ATTENDANCE_DIR = "attendance"

os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# ===================== VALIDATION =====================

if not os.path.exists(CROPPED_FACE_DIR):
    print("[ERROR] faces/cropped folder not found")
    exit()

if not os.path.exists(MODEL_PATH):
    print("[ERROR] face_model.yml not found")
    exit()

if not os.path.exists(LABELS_PATH):
    print("[ERROR] labels.txt not found")
    exit()

# ===================== LOAD LABELS =====================

label_map = {}
with open(LABELS_PATH, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, idx = line.split(":")
        label_map[int(idx)] = name

# ===================== LOAD MODEL =====================

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

# ===================== ATTENDANCE FILE =====================

today = datetime.now().strftime("%Y-%m-%d")
attendance_file = os.path.join(ATTENDANCE_DIR, f"attendance_{today}.csv")

marked = set()

if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])

# ===================== OFFLINE RECOGNITION =====================

print("[INFO] Offline face recognition started")

for img_name in os.listdir(CROPPED_FACE_DIR):
    img_path = os.path.join(CROPPED_FACE_DIR, img_name)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    img = cv2.resize(img, (200, 200))

    label, confidence = recognizer.predict(img)

    if confidence < 70:
        name = label_map.get(label, "Unknown")

        if name != "Unknown" and name not in marked:
            marked.add(name)

            time_now = datetime.now().strftime("%H:%M:%S")
            with open(attendance_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, today, time_now])

            print(f"[INFO] Attendance marked for {name}")
    else:
        print("[WARN] Unknown face:", img_name)

print("[INFO] Offline attendance completed")
