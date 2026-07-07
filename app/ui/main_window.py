"""
main_window.py

Main application window for SignSpeak.
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from collector_window import CollectorWindow
from recognition_window import RecognitionWindow


class MainWindow(QMainWindow):
    """
    Main window of the SignSpeak application.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SignSpeak")
        self.setMinimumSize(900, 700)

        self.collector_window = None
        self.recognition_window = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("SignSpeak")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size:36px;
            font-weight:bold;
        """)

        subtitle = QLabel(
            "Sign Language to Speech using Computer Vision"
        )

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle.setStyleSheet("""
            font-size:16px;
            color:gray;
        """)

        self.collector_button = QPushButton(
            "📸 Dataset Collector"
        )

        self.collector_button.setFixedSize(260, 55)

        self.collector_button.clicked.connect(
            self.open_collector
        )

        self.recognition_button = QPushButton(
            "🤖 Live Recognition"
        )

        self.recognition_button.setFixedSize(260, 55)

        self.recognition_button.clicked.connect(
            self.open_recognition
        )

        layout.addStretch()

        layout.addWidget(title)
        layout.addSpacing(15)

        layout.addWidget(subtitle)
        layout.addSpacing(45)

        layout.addWidget(
            self.collector_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addSpacing(20)

        layout.addWidget(
            self.recognition_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        layout.addStretch()

        central_widget.setLayout(layout)

    # -----------------------------------------
    # Dataset Collector
    # -----------------------------------------

    def open_collector(self):

        self.collector_window = CollectorWindow(parent=self)

        self.collector_window.destroyed.connect(
            self.collector_closed
        )

        self.hide()

        self.collector_window.show()

    def collector_closed(self):

        self.collector_window = None

        self.show()

        self.raise_()
        self.activateWindow()

    # -----------------------------------------
    # Live Recognition
    # -----------------------------------------

    def open_recognition(self):

        self.recognition_window = RecognitionWindow(parent=self)

        self.recognition_window.destroyed.connect(
            self.recognition_closed
        )

        self.hide()

        self.recognition_window.show()

    def recognition_closed(self):

        self.recognition_window = None

        self.show()

        self.raise_()
        self.activateWindow()


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()