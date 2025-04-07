import os.path
import threading
import time
import mediapipe as mp
import cv2
from src.app.config import load_settings
from src.app.db_queries import add_image
from src.app.database import SessionLocal
from src.app.events import Events
from src.app.schemas import Image

DETECTION_INTERVAL = 5

class Camera:
    def __init__(self):
        self.settings = load_settings()
        self.running = False
        self.thread = None
        self.person_detected = False
        self.timer_start_time = None
        self.db = SessionLocal()

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _capture_frames(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                if self._detect_person(frame):
                    if not self.person_detected:
                        self.person_detected = True
                        self.timer_start_time = time.time()
                    elif time.time() - self.timer_start_time >= DETECTION_INTERVAL:
                        self._save_image(frame)
                        self.person_detected = False
                else:
                    self.person_detected = False
        cap.release()

    def _detect_person(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            image_height, image_width, _ = frame.shape

            x, y, width, height = (
                self.settings["x"],
                self.settings["y"],
                self.settings["width"],
                self.settings["height"],
            )

            for landmark in results.pose_landmarks.landmark:
                landmark_x = int(landmark.x * image_width)
                landmark_y = int(landmark.y * image_height)

                if x <= landmark_x <= x + width and y <= landmark_y <= y + height:
                    return True

        return False

    def _save_image(self, frame):
        timestamp = int(time.time())
        photo_path = f"images/person_{timestamp}.jpg"
        abs_path = os.path.abspath(photo_path)
        cv2.imwrite(abs_path, frame)
        add_image(self.db, Image(file_path=abs_path))
        Events.change_image_path(abs_path)

