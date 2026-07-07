"""
camera.py

Handles all webcam interactions for SignSpeak.
"""

import cv2


class Camera:
    """
    Camera module responsible for opening,
    reading, and releasing the webcam.
    """

    def __init__(self):
        """
        Initializes the webcam.
        """

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        print("Camera initialized.")

    def get_frame(self):
        """
        Captures and returns a single frame from the webcam.
        """

        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Failed to capture frame from webcam.")

        # Flip the frame horizontally (mirror view)
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        """
        Releases the webcam resources.
        """

        if self.cap.isOpened():
            self.cap.release()

        print("Camera released.")