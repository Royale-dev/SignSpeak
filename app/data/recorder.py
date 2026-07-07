"""
recorder.py

Records labeled hand landmark data into a CSV dataset.
"""

import csv
from pathlib import Path


class Recorder:
    """
    Records hand landmarks into a CSV file.
    """

    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)

        # Create the directory if it doesn't exist
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        # Create the CSV file with a header if needed
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            self._write_header()

    def _write_header(self):
        """
        Writes the CSV header.
        """

        header = ["label"]

        for i in range(21):
            header.extend([
                f"x{i}",
                f"y{i}",
                f"z{i}"
            ])

        with self.csv_path.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)

    def save_sample(self, label, hand):
        """
        Saves one labeled hand sample to the dataset.
        """

        row = [label]

        # Flatten the 21 landmarks into the row
        for landmark in hand.landmarks:
            row.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        with self.csv_path.open("a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)