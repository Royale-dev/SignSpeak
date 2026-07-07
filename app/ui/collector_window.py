"""
collector_window.py

Dataset Collector window with reset dataset support.
"""

import cv2
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from camera.camera import Camera
from vision.hand_detector import HandDetector
from data.collector import Collector

from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QMessageBox,
)

from camera_view import CameraView
from status_panel import StatusPanel
from control_panel import ControlPanel
from dialogs.label_dialog import LabelDialog
from dialogs.dataset_progress_dialog import DatasetProgressDialog


class CollectorWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("SignSpeak - Dataset Collector")
        self.resize(1400, 850)

        self.camera = Camera()
        self.detector = HandDetector()

        self.collector = Collector(
            csv_path="datasets/raw/landmarks.csv",
            initial_label="A",
            target_samples=300,
        )

        self.prev_time = time.time()
        self.progress_dialog = None

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        self.camera_view = CameraView()
        root.addWidget(self.camera_view, stretch=3)

        right = QVBoxLayout()

        self.status_panel = StatusPanel()
        self.status_panel.set_label(self.collector.current_label)
        self.status_panel.set_samples(self.collector.samples_saved)
        self.status_panel.set_status(self.collector.status)

        self.control_panel = ControlPanel()

        self.control_panel.start_button.clicked.connect(
            self.collector.start_capture
        )

        self.control_panel.label_button.clicked.connect(
            self.change_label
        )

        self.control_panel.progress_button.clicked.connect(
            self.show_progress_dialog
        )

        self.control_panel.reset_button.clicked.connect(
            self.reset_dataset
        )

        self.control_panel.back_button.clicked.connect(
            self.go_back
        )

        right.addWidget(self.status_panel)
        right.addSpacing(15)
        right.addWidget(self.control_panel)

        root.addLayout(right, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
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

    def show_progress_dialog(self):

        if self.progress_dialog is None:
            self.progress_dialog = DatasetProgressDialog(
                self.collector,
                self,
            )

        self.progress_dialog.show()
        self.progress_dialog.raise_()
        self.progress_dialog.activateWindow()

    # --------------------------------------------------

    def reset_dataset(self):

        reply = QMessageBox.question(
            self,
            "Reset Dataset",
            "This will permanently delete landmarks.csv and progress.json.\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        self.collector.reset_dataset()

        self.status_panel.set_label(
            self.collector.current_label
        )

        self.status_panel.set_samples(
            self.collector.samples_saved
        )

        self.status_panel.set_status(
            self.collector.status
        )

        if self.progress_dialog is not None:
            self.progress_dialog.refresh()

    # --------------------------------------------------

    def change_label(self):

        dialog = LabelDialog(
            current_label=self.collector.current_label,
            parent=self,
        )

        if dialog.exec():

            if self.collector.change_label(
                dialog.selected_label()
            ):

                self.status_panel.set_label(
                    self.collector.current_label
                )

                self.status_panel.set_samples(
                    self.collector.samples_saved
                )

                self.status_panel.set_status(
                    self.collector.status
                )

    # --------------------------------------------------

    def draw_overlay(self, frame):

        h, w = frame.shape[:2]

        if self.collector.countdown_active:

            txt = str(
                self.collector.remaining_countdown
            )

            size = cv2.getTextSize(
                txt,
                cv2.FONT_HERSHEY_SIMPLEX,
                4,
                6,
            )[0]

            cv2.putText(
                frame,
                txt,
                ((w - size[0]) // 2, (h + size[1]) // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                4,
                (0, 0, 255),
                6,
            )

        elif self.collector.capturing:

            txt = (
                f"{self.collector.capture_progress}/"
                f"{self.collector.BURST_SIZE}"
            )

            size = cv2.getTextSize(
                txt,
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                4,
            )[0]

            cv2.putText(
                frame,
                txt,
                ((w - size[0]) // 2, (h + size[1]) // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 0),
                4,
            )

    # --------------------------------------------------

    def update_camera(self):

        frame = self.camera.get_frame()

        results = self.detector.detect(frame)
        frame = self.detector.draw(frame, results)

        hands = self.detector.get_hands(results)

        self.collector.update(hands)

        self.draw_overlay(frame)

        self.status_panel.set_samples(
            self.collector.samples_saved
        )

        self.status_panel.set_status(
            self.collector.status
        )

        now = time.time()

        fps = 1.0 / max(
            now - self.prev_time,
            1e-6,
        )

        self.prev_time = now

        self.status_panel.set_fps(fps)

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