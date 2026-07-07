"""
label_dialog.py

Dialog for selecting a valid ASL label.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class LabelDialog(QDialog):
    """
    Dialog used to choose an ASL label (A-Z).
    """

    VALID_LABELS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self, current_label="A", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change Label")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        title = QLabel("Select Gesture Label")
        title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(title)

        self.combo = QComboBox()
        self.combo.addItems(self.VALID_LABELS)

        index = self.combo.findText(current_label.upper())
        if index >= 0:
            self.combo.setCurrentIndex(index)

        self.combo.setStyleSheet("font-size:16px;")
        layout.addWidget(self.combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def selected_label(self):
        """
        Returns the selected ASL label.
        """
        return self.combo.currentText()
