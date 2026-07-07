"""
control_panel.py

Collector controls.
"""

from PySide6.QtWidgets import (
    QPushButton,
    QFrame,
    QVBoxLayout,
)


class ControlPanel(QFrame):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # -----------------------------
        # Start Burst
        # -----------------------------
        self.start_button = QPushButton("🟢  Start Burst")
        self.start_button.setMinimumHeight(55)
        self.start_button.setStyleSheet("""
            QPushButton{
                background-color:#2E7D32;
                color:white;
                font-size:16px;
                font-weight:bold;
                border-radius:8px;
            }

            QPushButton:hover{
                background-color:#388E3C;
            }
        """)

        # -----------------------------
        # Change Label
        # -----------------------------
        self.label_button = QPushButton("🏷  Change Label")
        self.label_button.setMinimumHeight(50)
        self.label_button.setStyleSheet("""
            font-size:15px;
        """)

        # -----------------------------
        # Dataset Progress
        # -----------------------------
        self.progress_button = QPushButton("📊  Dataset Progress")
        self.progress_button.setMinimumHeight(50)
        self.progress_button.setStyleSheet("""
            font-size:15px;
        """)

        # -----------------------------
        # Reset Dataset
        # -----------------------------
        self.reset_button = QPushButton("🗑  Reset Dataset")
        self.reset_button.setMinimumHeight(50)
        self.reset_button.setStyleSheet("""
            QPushButton{
                background-color:#C62828;
                color:white;
                font-size:15px;
                font-weight:bold;
                border-radius:8px;
            }

            QPushButton:hover{
                background-color:#D32F2F;
            }
        """)

        layout.addWidget(self.start_button)
        layout.addWidget(self.label_button)
        layout.addWidget(self.progress_button)
        layout.addWidget(self.reset_button)

        layout.addStretch()

        # -----------------------------
        # Back
        # -----------------------------
        self.back_button = QPushButton("⬅  Back")
        self.back_button.setMinimumHeight(45)

        layout.addWidget(self.back_button)
