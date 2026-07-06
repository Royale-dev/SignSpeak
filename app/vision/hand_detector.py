"""
hand_detector.py

Handles hand detection using MediaPipe.
"""

import cv2
import mediapipe as mp

from vision.hand import Hand


class HandDetector:
    """
    Detects and tracks hands using MediaPipe.
    """

    def __init__(self):
        """
        Initializes the MediaPipe Hands solution.
        """

        # MediaPipe Hands module
        self.mp_hands = mp.solutions.hands

        # Hand detector object
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # Utility used later for drawing landmarks
        self.mp_drawing = mp.solutions.drawing_utils

    def detect(self, frame):
        """
        Detects hands in a webcam frame.

        Parameters
        ----------
        frame : numpy.ndarray
            Frame captured from the webcam (BGR).

        Returns
        -------
        results
            MediaPipe detection results.
        """

        # Convert OpenCV's BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run hand detection
        results = self.hands.process(rgb_frame)

        return results

    def draw(self, frame, results):
        """
        Draws detected hand landmarks on the frame.

        Parameters
        ----------
        frame : numpy.ndarray
            Webcam frame.

        results
            MediaPipe detection results.

        Returns
        -------
        numpy.ndarray
            Frame with landmarks drawn.
        """

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

        return frame

    def get_hands(self, results):
        """
        Returns a list of detected Hand objects.
        """

        detected_hands = []

        if not results.multi_hand_landmarks:
            return detected_hands

        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):

            hand = Hand(
                label=handedness.classification[0].label,
                confidence=handedness.classification[0].score,
                landmarks=hand_landmarks,
            )

            detected_hands.append(hand)

        return detected_hands

    def count_hands(self, results):
        """
        Returns the number of detected hands.
        """

        return len(self.get_hands(results))