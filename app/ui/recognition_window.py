"""
recognition_window_v6_speak_20260707.py

Recognition window for SignSpeak.
Includes:
- Prediction stabilizer
- Blank hand detection
- Letter buffer
- Backspace / Space / Clear controls
- Text-to-Speech
"""

import sys
import time
from pathlib import Path

import cv2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from camera.camera import Camera
from vision.hand_detector import HandDetector
from ml.predictor import Predictor
from ml.prediction_stabilizer import PredictionStabilizer
from ml.blank_hand_detector import BlankHandDetector
from ml.letter_buffer import LetterBuffer
from ml.tts import TextToSpeech

from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QMainWindow,
    QPushButton,
)

from camera_view import CameraView


class RecognitionWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("SignSpeak - Live Recognition")
        self.resize(1400, 850)

        self.camera = Camera()
        self.detector = HandDetector()
        self.predictor = Predictor()
        self.stabilizer = PredictionStabilizer(window_size=10, threshold=8)
        self.blank_detector = BlankHandDetector()
        self.letter_buffer = LetterBuffer()
        self.tts = TextToSpeech()

        self.prev_time = time.time()

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        self.camera_view = CameraView()
        root.addWidget(self.camera_view, stretch=3)

        panel = QFrame()
        panel_layout = QVBoxLayout(panel)

        title = QLabel("Live Recognition")
        title.setStyleSheet("font-size:26px;font-weight:bold;")

        self.prediction = QLabel("-")
        self.prediction.setStyleSheet(
            "font-size:64px;font-weight:bold;color:#4FC3F7;"
        )

        self.recognized = QLabel("")
        self.recognized.setWordWrap(True)
        self.recognized.setStyleSheet(
            "font-size:28px;font-weight:bold;color:#FFFFFF;"
        )

        self.confidence = QLabel("Confidence: --")
        self.confidence.setStyleSheet("font-size:20px;")

        self.status = QLabel("No Hand")
        self.status.setStyleSheet("font-size:20px;color:#FFC107;")

        self.fps = QLabel("FPS: 0.0")
        self.fps.setStyleSheet("font-size:18px;")

        self.back_button = QPushButton("⬅ Back")
        self.backspace_button = QPushButton("⌫ Backspace")
        self.space_button = QPushButton("Space")
        self.clear_button = QPushButton("🗑 Clear")
        self.speak_button = QPushButton("🔊 Speak")

        self.back_button.clicked.connect(self.go_back)
        self.backspace_button.clicked.connect(self.backspace_text)
        self.space_button.clicked.connect(self.add_space)
        self.clear_button.clicked.connect(self.clear_text)
        self.speak_button.clicked.connect(self.speak_text)

        panel_layout.addWidget(title)
        panel_layout.addSpacing(20)
        panel_layout.addWidget(QLabel("Prediction"))
        panel_layout.addWidget(self.prediction)

        panel_layout.addSpacing(15)
        panel_layout.addWidget(QLabel("Recognized Text"))
        panel_layout.addWidget(self.recognized)

        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.confidence)

        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.status)

        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.fps)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        grid.addWidget(self.backspace_button, 0, 0)
        grid.addWidget(self.space_button, 0, 1)
        grid.addWidget(self.clear_button, 1, 0)
        grid.addWidget(self.speak_button, 1, 1)

        panel_layout.addSpacing(20)
        panel_layout.addLayout(grid)

        panel_layout.addStretch()
        panel_layout.addWidget(self.back_button)

        root.addWidget(panel, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)

    def refresh_text(self):
        self.recognized.setText(self.letter_buffer.get_text())

    def backspace_text(self):
        self.letter_buffer.backspace()
        self.refresh_text()

    def add_space(self):
        self.letter_buffer.add_space()
        self.refresh_text()

    def clear_text(self):
        self.letter_buffer.clear()
        self.refresh_text()

    def speak_text(self):
        self.tts.speak(self.letter_buffer.get_text())

    def go_back(self):
        parent = self.parent()
        if parent is not None:
            parent.show()
            parent.raise_()
            parent.activateWindow()
        self.close()

    def update_camera(self):
        frame = self.camera.get_frame()

        results = self.detector.detect(frame)
        frame = self.detector.draw(frame, results)
        hands = self.detector.get_hands(results)

        if hands:
            try:
                label, conf = self.predictor.predict(hands[0])
                stable = self.stabilizer.update(label)

                self.prediction.setText(stable if stable else "-")
                self.confidence.setText(f"Confidence: {conf:.2f}%")
                self.status.setText("Hand Detected")
                self.status.setStyleSheet("font-size:20px;color:#4CAF50;")

                committed = self.blank_detector.update(True, stable)
                if committed:
                    self.letter_buffer.add_letter(committed)
                    self.refresh_text()

            except Exception as e:
                self.prediction.setText("-")
                self.confidence.setText("Confidence: --")
                self.status.setText(str(e))
                self.status.setStyleSheet("font-size:20px;color:red;")
        else:
            committed = self.blank_detector.update(False, None)
            if committed:
                self.letter_buffer.add_letter(committed)
                self.refresh_text()

            self.stabilizer.reset()

            self.prediction.setText("-")
            self.confidence.setText("Confidence: --")
            self.status.setText("No Hand")
            self.status.setStyleSheet("font-size:20px;color:#FFC107;")

        now = time.time()
        fps = 1.0 / max(now - self.prev_time, 1e-6)
        self.prev_time = now
        self.fps.setText(f"FPS: {fps:.1f}")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.camera_view.set_pixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.timer.stop()
        self.camera.release()
        event.accept()
