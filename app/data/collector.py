"""
collector.py

Qt-native dataset collector with per-label progress,
automatic progress persistence and dataset reset support.
"""

import json
import os
import time
from pathlib import Path

from .recorder import Recorder


class Collector:

    COUNTDOWN_SECONDS = 3
    STATUS_DURATION = 1.0
    BURST_SIZE = 30

    VALID_LABELS = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self, csv_path, initial_label="A", target_samples=300):

        # ----------------------------------------
        # Absolute project paths
        # ----------------------------------------

        self.project_root = Path(__file__).resolve().parent.parent.parent

        self.csv_path = self.project_root / csv_path
        self.progress_path = self.csv_path.parent / "progress.json"

        self.recorder = Recorder(str(self.csv_path))

        self.target_samples = target_samples
        self.label = initial_label

        self.label_counts = {
            label: 0 for label in self.VALID_LABELS
        }

        self.load_progress()

        self.status = "READY"
        self.status_start_time = time.time()

        self.countdown_active = False
        self.countdown_start_time = 0.0

        self.capturing = False
        self.capture_count = 0

    # --------------------------------------------------
    # Progress
    # --------------------------------------------------

    def load_progress(self):

        if not self.progress_path.exists():
            return

        try:

            with open(self.progress_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for label in self.VALID_LABELS:
                self.label_counts[label] = int(
                    data.get(label, 0)
                )

            print("Loaded dataset progress.")

        except Exception as e:
            print("Could not load progress:", e)

    def save_progress(self):

        try:

            self.progress_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                self.progress_path,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    self.label_counts,
                    f,
                    indent=4,
                )

        except Exception as e:
            print("Could not save progress:", e)

    # --------------------------------------------------
    # Reset Dataset
    # --------------------------------------------------

    def reset_dataset(self):
        """
        Completely resets the dataset.
        """

        try:

            if self.csv_path.exists():
                os.remove(self.csv_path)
                print("Deleted:", self.csv_path)

            if self.progress_path.exists():
                os.remove(self.progress_path)
                print("Deleted:", self.progress_path)

            self.label_counts = {
                label: 0
                for label in self.VALID_LABELS
            }

            self.label = "A"

            self.capture_count = 0
            self.countdown_active = False
            self.capturing = False

            self.set_status("READY")

            self.recorder = Recorder(str(self.csv_path))

            print("Dataset reset successfully.")

        except Exception as e:
            print("Reset failed:", e)

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def set_status(self, status):

        self.status = status
        self.status_start_time = time.time()

    # --------------------------------------------------
    # Capture
    # --------------------------------------------------

    def start_capture(self):

        if self.countdown_active or self.capturing:
            return False

        if self.samples_saved >= self.target:
            self.set_status("COMPLETE")
            return False

        self.countdown_active = True
        self.countdown_start_time = time.time()

        self.set_status("COUNTDOWN")

        return True

    def change_label(self, label):

        label = label.strip().upper()

        if label not in self.VALID_LABELS:
            raise ValueError("Invalid label.")

        if self.countdown_active or self.capturing:
            return False

        self.label = label

        if self.samples_saved >= self.target:
            self.set_status("COMPLETE")
        else:
            self.set_status("READY")

        return True

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, hands):

        now = time.time()

        if (
            self.status == "SAVED!"
            and now - self.status_start_time
            >= self.STATUS_DURATION
        ):

            if self.samples_saved >= self.target:
                self.set_status("COMPLETE")
            else:
                self.set_status("READY")

        if self.countdown_active:

            if self.remaining_countdown <= 0:

                self.countdown_active = False
                self.capturing = True
                self.capture_count = 0

                self.set_status("CAPTURING")

            return

        if not self.capturing:
            return

        if self.samples_saved >= self.target:

            self.capturing = False
            self.set_status("COMPLETE")
            return

        if hands:

            self.recorder.save_sample(
                self.label,
                hands[0],
            )

            self.capture_count += 1
            self.label_counts[self.label] += 1

        if (
            self.capture_count >= self.BURST_SIZE
            or self.samples_saved >= self.target
        ):

            self.capturing = False

            self.save_progress()

            if self.samples_saved >= self.target:
                self.set_status("COMPLETE")
            else:
                self.set_status("SAVED!")

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def samples_saved(self):
        return self.label_counts[self.label]

    @property
    def total_samples(self):
        return sum(self.label_counts.values())

    @property
    def current_label(self):
        return self.label

    @property
    def remaining_countdown(self):

        if not self.countdown_active:
            return 0

        return self.COUNTDOWN_SECONDS - int(
            time.time() - self.countdown_start_time
        )

    @property
    def capture_progress(self):
        return self.capture_count

    @property
    def target(self):
        return self.target_samples