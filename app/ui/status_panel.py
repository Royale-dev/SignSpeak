"""
status_panel.py

Displays collector information.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QProgressBar,
)


class StatusPanel(QFrame):
    """
    Displays collector status information.
    """

    TARGET_SAMPLES = 300

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(340)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # -----------------------------
        # Title
        # -----------------------------
        title = QLabel("Dataset Information")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addSpacing(15)

        # -----------------------------
        # Current Label
        # -----------------------------
        label_title = QLabel("Current Label")
        label_title.setStyleSheet("""
            color:gray;
            font-size:14px;
        """)

        self.label = QLabel("A")
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setStyleSheet("""
            font-size:52px;
            font-weight:bold;
            color:#4FC3F7;
        """)

        layout.addWidget(label_title)
        layout.addWidget(self.label)

        # -----------------------------
        # Samples
        # -----------------------------
        samples_title = QLabel("Samples")
        samples_title.setStyleSheet("""
            color:gray;
            font-size:14px;
        """)

        self.samples = QLabel("0 / 300")
        self.samples.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(samples_title)
        layout.addWidget(self.samples)

        # -----------------------------
        # Progress Bar
        # -----------------------------
        self.progress = QProgressBar()

        self.progress.setMinimum(0)
        self.progress.setMaximum(self.TARGET_SAMPLES)
        self.progress.setValue(0)

        self.progress.setTextVisible(False)

        self.progress.setFixedHeight(16)

        layout.addWidget(self.progress)

        # -----------------------------
        # Status
        # -----------------------------
        status_title = QLabel("Status")
        status_title.setStyleSheet("""
            color:gray;
            font-size:14px;
        """)

        self.status = QLabel("READY")

        self.status.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#4CAF50;
        """)

        layout.addSpacing(10)

        layout.addWidget(status_title)
        layout.addWidget(self.status)

        # -----------------------------
        # FPS
        # -----------------------------
        fps_title = QLabel("Processing FPS")
        fps_title.setStyleSheet("""
            color:gray;
            font-size:14px;
        """)

        self.fps = QLabel("0.0")

        self.fps.setStyleSheet("""
            font-size:18px;
        """)

        layout.addSpacing(10)

        layout.addWidget(fps_title)
        layout.addWidget(self.fps)

        layout.addStretch()

    # --------------------------------------------------
    # Update Functions
    # --------------------------------------------------

    def set_label(self, label):
        self.label.setText(label)

    def set_samples(self, samples):
        self.samples.setText(
            f"{samples} / {self.TARGET_SAMPLES}"
        )

        self.progress.setValue(samples)

    def set_status(self, status):

        colors = {
            "READY": "#4CAF50",
            "COUNTDOWN": "#FFC107",
            "CAPTURING": "#FF9800",
            "SAVED!": "#42A5F5",
            "ERROR": "#F44336",
        }

        self.status.setText(status)

        color = colors.get(status, "white")

        self.status.setStyleSheet(f"""
            font-size:20px;
            font-weight:bold;
            color:{color};
        """)

    def set_fps(self, fps):
        self.fps.setText(f"{fps:.1f}")