"""
camera_view.py

Camera display widget.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout


class CameraView(QFrame):
    """
    Displays the live camera feed.
    """

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)

        title = QLabel("📷 Live Camera")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        self.camera_label = QLabel()

        self.camera_label.setAlignment(Qt.AlignCenter)

        self.camera_label.setText(
            "Waiting for camera..."
        )

        self.camera_label.setStyleSheet("""
            border:2px solid #444;
            border-radius:8px;
            background-color:#202020;
            color:gray;
            font-size:24px;
        """)

        layout.addWidget(
            self.camera_label,
            stretch=1
        )

    def set_pixmap(self, pixmap: QPixmap):
        """
        Displays the latest camera frame.
        """

        self.camera_label.setPixmap(
            pixmap.scaled(
                self.camera_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )