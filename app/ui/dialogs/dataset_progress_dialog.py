"""
dataset_progress_dialog.py

Shows progress for all ASL labels.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QScrollArea,
    QWidget,
)


class DatasetProgressDialog(QDialog):
    def __init__(self, collector, parent=None):
        super().__init__(parent)

        self.collector = collector

        self.setWindowTitle("Dataset Progress")
        self.resize(500, 700)

        root = QVBoxLayout(self)

        title = QLabel("Dataset Progress")
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        root.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.rows = {}

        for label in collector.VALID_LABELS:
            row = QHBoxLayout()

            lbl = QLabel(label)
            lbl.setFixedWidth(25)

            bar = QProgressBar()
            bar.setMaximum(collector.target)

            value = QLabel()

            row.addWidget(lbl)
            row.addWidget(bar)
            row.addWidget(value)

            self.layout.addLayout(row)

            self.rows[label] = (bar, value)

        self.layout.addStretch()

        scroll.setWidget(container)
        root.addWidget(scroll)

        self.total_label = QLabel()
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )
        root.addWidget(self.total_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(200)

        self.refresh()

    def refresh(self):
        total = 0

        for label in self.collector.VALID_LABELS:
            count = self.collector.label_counts[label]
            total += count

            bar, value = self.rows[label]
            bar.setValue(count)
            value.setText(f"{count}/{self.collector.target}")

        overall = len(self.collector.VALID_LABELS) * self.collector.target

        self.total_label.setText(
            f"Overall: {total} / {overall}"
        )
