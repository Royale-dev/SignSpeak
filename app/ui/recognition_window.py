"""
recognition_window.py

Live recognition window for SignSpeak.
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

from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
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

        self.prev_time = time.time()

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        self.camera_view = CameraView()
        root.addWidget(self.camera_view, stretch=3)

        panel = QFrame()
        panel_layout = QVBoxLayout(panel)

        title = QLabel("Live Recognition")
        title.setStyleSheet(
            "font-size:26px;font-weight:bold;"
        )

        self.prediction = QLabel("-")
        self.prediction.setStyleSheet(
            "font-size:64px;font-weight:bold;color:#4FC3F7;"
        )

        self.confidence = QLabel("Confidence: --")
        self.confidence.setStyleSheet(
            "font-size:20px;"
        )

        self.status = QLabel("No Hand")
        self.status.setStyleSheet(
            "font-size:20px;color:#FFC107;"
        )

        self.fps = QLabel("FPS: 0.0")
        self.fps.setStyleSheet(
            "font-size:18px;"
        )

        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(
            self.go_back
        )

        panel_layout.addWidget(title)
        panel_layout.addSpacing(20)

        panel_layout.addWidget(QLabel("Prediction"))
        panel_layout.addWidget(self.prediction)

        panel_layout.addSpacing(10)

        panel_layout.addWidget(self.confidence)

        panel_layout.addSpacing(10)

        panel_layout.addWidget(self.status)

        panel_layout.addSpacing(10)

        panel_layout.addWidget(self.fps)

        panel_layout.addStretch()

        panel_layout.addWidget(self.back_button)

        root.addWidget(panel, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update_camera
        )
        self.timer.start(30)

    # --------------------------------------------------

    def go_back(self):
        """
        Return to the main menu.
        """

        parent = self.parent()

        if parent is not None:
            parent.show()
            parent.raise_()
            parent.activateWindow()

        self.close()

    # --------------------------------------------------

    def update_camera(self):

        frame = self.camera.get_frame()

        results = self.detector.detect(frame)
        frame = self.detector.draw(frame, results)

        hands = self.detector.get_hands(results)

        if hands:
            try:
                label, conf = self.predictor.predict(
                    hands[0]
                )

                self.prediction.setText(label)

                self.confidence.setText(
                    f"Confidence: {conf:.2f}%"
                )

                self.status.setText(
                    "Hand Detected"
                )

                self.status.setStyleSheet(
                    "font-size:20px;color:#4CAF50;"
                )

            except Exception as e:

                self.prediction.setText("-")

                self.confidence.setText(
                    "Confidence: --"
                )

                self.status.setText(str(e))

                self.status.setStyleSheet(
                    "font-size:20px;color:red;"
                )

        else:

            self.prediction.setText("-")

            self.confidence.setText(
                "Confidence: --"
            )

            self.status.setText(
                "No Hand"
            )

            self.status.setStyleSheet(
                "font-size:20px;color:#FFC107;"
            )

        now = time.time()

        fps = 1.0 / max(
            now - self.prev_time,
            1e-6,
        )

        self.prev_time = now

        self.fps.setText(
            f"FPS: {fps:.1f}"
        )

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        h, w, ch = rgb.shape

        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888,
        )

        self.camera_view.set_pixmap(
            QPixmap.fromImage(image)
        )

    # --------------------------------------------------

    def closeEvent(self, event):

        self.timer.stop()

        self.camera.release()

        event.accept()