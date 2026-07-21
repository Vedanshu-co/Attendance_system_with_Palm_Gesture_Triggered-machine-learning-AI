# Attendance_system_with_Palm_Gesture_Triggered-machine-learning-AI
The system uses a palm gesture as a trigger to capture the user’s face. The captured face is processed using OpenCV and recognized using an LBPH model. If the face matches a known user, attendance is recorded in a CSV file and uploaded to Firebase. The system uses LEDs to indicate different stages such as detection, processing, and completion


🚀 How to Use

Follow these steps to set up and run the project:

1. Clone the Repository

git clone https://github.com/Vedanshu-co/Student_attendance_modifiocation01.git
cd Student_attendance_modifiocation01

2. Create and Activate a Virtual Environment

python3 -m venv vision_env
source vision_env/bin/activate

3. Install the Required Dependencies

pip install -r requirements.txt

4. Configure the Hardware

* Connect the Raspberry Pi Camera or IR Camera.
* Connect the Red, Yellow, and Green LEDs to the configured GPIO pins.
* Ensure the camera is enabled in Raspberry Pi OS.
* Place the trained face recognition model (face_model.yml) and labels.txt in the models/ directory.

5. Configure Firebase (Optional)

* Create a Firebase project.
* Download the Firebase Admin SDK service account key.
* Place the JSON key file in the project directory.
* Update the Firebase configuration in upload_to_firebase.py.

6. Run the Application

Start the complete attendance system:

python run.py

Or, if using MJPEG streaming with rpicam-vid:

rpicam-vid -t 0 --codec mjpeg --width 1280 --height 720 --framerate 25 --nopreview -o - | python3 palm_face_capture.py

7. System Workflow

1. Show your palm to the camera to trigger the system.
2. Wait for the countdown to finish.
3. Face detection and recognition will run automatically.
4. Attendance will be recorded in a CSV file.
5. Attendance data will be uploaded to Firebase Firestore (if configured).
6. The LEDs indicate the current status of the process.

8. Output

* Attendance records are saved in the attendance/ folder.
* Captured face images are stored in the faces/ folder.
* Attendance data is uploaded to Firebase Firestore after successful recognition.

Notes

* Use good lighting for better face detection accuracy.
* Ensure the trained model and label files are available before running the application.
* Verify all required Python packages are installed from requirements.txt.
* Confirm that the Raspberry Pi camera and GPIO connections are functioning correctly before starting the system.


# problem faced
IoT-based Face Detection and Attendance System using Raspberry Pi 3B+, IR Camera, MediaPipe, OpenCV, and Firebase.

1. Hardware Problems

Raspberry Pi Camera Detection

* Camera was not detected initially.
* Errors like:
    * supported=1 detected=0
    * failed to acquire camera
* Loose camera ribbon cable and configuration issues.
* Camera interface had to be enabled and tested multiple times.

IR Camera Issues

* Switched from a normal camera to an IR camera.
* Different image quality affected face detection.
* Brightness and exposure required adjustment.

Raspberry Pi Performance

* Raspberry Pi 3B+ has limited CPU and RAM.
* Face recognition became slow when multiple processes ran simultaneously.
* High CPU usage caused lag during live streaming.

⸻

2. Operating System Problems

You tried multiple Raspberry Pi OS versions:

* Bullseye Legacy
* Trixie
* Bookworm

Problems included:

* Camera drivers behaving differently.
* Missing packages.
* Library incompatibility.
* Different libcamera versions.

⸻

3. Python Version Compatibility

You experienced compatibility issues because:

* Python 3.13 was not supported by several libraries.
* MediaPipe compatibility was poor.
* Needed Python 3.11.

This required:

* Creating a virtual environment.
* Installing compatible package versions.

⸻

4. MediaPipe Installation Problems

Major issues:

* ModuleNotFoundError
* Version conflicts
* Missing wheel files
* Installation failures

You also encountered protobuf conflicts.
_____

5. NumPy Compatibility

Problems:

* NumPy 2.x incompatible with MediaPipe.
* Downgrading NumPy caused dependency conflicts with other packages.
* Multiple reinstallations were needed.
______

7. Camera Streaming Problems

Initially:

* Picamera2
* OpenCV camera capture

didn’t perform reliably.
Problems included:

* Broken pipe
* Frame loss
* Buffer delay
* Incorrect MJPEG decoding
______

8. Face Detection Problems

False Detection

Sometimes:

* Background objects were detected.
* Multiple boxes appeared around one face.

⸻

Missed Detection

Faces were not detected because of:

* Low lighting
* IR image quality
* Small face size
* Side face
* Tilted head

⸻

Multiple Faces

Initially only one face was saved.

Requirement:

* Detect all faces.
* Save every cropped face separately.

Code had to be modified.

⸻

9. Palm Gesture Integration Problems

Since your system starts only after palm detection:

Problems:

* Palm not detected correctly.
* Countdown restarting.
* Gesture lost midway.
* False triggering.

Synchronization with face detection was difficult.

⸻

10. Image Saving Problems

Problems included:

* Cropped image not saved.
* Full image missing.
* Wrong directory.
* Duplicate filenames.
* Images overwritten.

You later implemented timestamp-based filenames.

_____

11. Face Recognition Problems

Recognition issues:

* Unknown faces.
* Wrong person identified.
* Confidence threshold tuning.
* Lighting differences.
* Different facial expressions.
_____

12. Model File Problems

Files:
face_model.yml
labels.txt
Problems:

Problems:

* Incorrect label mapping.
* Missing labels.
* Wrong label format.
* File path issues.

⸻

13. Attendance CSV Problems

Issues:

* Duplicate attendance entries.
* Wrong timestamp.
* Missing roll number.
* CSV format mismatch.
* Upload script unable to read columns.

⸻

14. Firebase Upload Problems

Problems:

* Authentication configuration.
* Incorrect JSON credential path.
* Firestore document structure mismatch.
* CSV parsing errors.
* Failed uploads.

⸻

15. LED Synchronization Problems

Desired sequence:

* Red → Palm detected
* Yellow → Capturing
* Green → Attendance marked
* Blink → Upload complete

Problems:

* LEDs blinking incorrectly.
* GPIO timing issues.
* LEDs remaining ON after script ended.
_____

16. File Structure Problems

Several scripts depended on:
models/
attendance/
faces/
cascades/

Problems:

* Missing folders.
* Wrong paths.
* Relative path errors.

⸻

17. Script Integration Problems

Your project consisted of multiple scripts:

* Palm detection
* Face recognition
* Attendance generation
* Firebase upload

Challenges:

* Running them in the correct order.
* Passing data between scripts.
* Handling failures gracefully.

⸻

18. OpenCV Problems

Issues included:

* Haar Cascade XML not found.
* OpenCV version mismatch.
* Frame conversion errors.
* Slow detection on Raspberry Pi.

⸻

19. Code Errors

You encountered:

* TabError
* IndentationError
* ModuleNotFoundError
* ImportError
* FileNotFoundError
* AttributeError
* Broken pipe errors

These required repeated debugging.

⸻

20. Performance Problems

Real-time execution suffered due to:

* High CPU utilization.
* Low FPS.
* Detection delay.
* Recognition latency.
* Slow CSV writing.
* Upload waiting time.

⸻

21. Overall System Integration Challenges

The biggest challenge was integrating all components into a single automated pipeline:

1. Palm gesture detection
2. Countdown
3. Face detection
4. Face cropping
5. Face recognition
6. Attendance generation
7. CSV creation
8. Firebase upload
9. LED status indication

Ensuring each stage triggered correctly without conflicts required extensive testing and debugging.
