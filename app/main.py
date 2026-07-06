"""
main.py

Entry point for the SignSpeak application.
"""

import cv2
import time
from collections import deque

from camera.camera import Camera
from vision.hand_detector import HandDetector


def main():
    """
    Starts the SignSpeak application.
    """

    # Initialize modules
    camera = Camera()
    detector = HandDetector()

    # Used to calculate FPS
    prev_time = time.time()

    # Store the last 30 FPS values
    fps_history = deque(maxlen=30)

    while True:

        # Capture one frame
        frame = camera.get_frame()

        # Detect hands
        results = detector.detect(frame)

        # Draw detected landmarks
        frame = detector.draw(frame, results)

        # Convert MediaPipe results into Hand objects
        hands = detector.get_hands(results)

        # -----------------------------
        # Display hand information
        # -----------------------------
        if hands:

            hand = hands[0]

            cv2.putText(
                frame,
                f"Hands Detected: {len(hands)}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Hand: {hand.label}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Index : {hand.index_is_up}",
                (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Middle: {hand.middle_is_up}",
                (10, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Ring  : {hand.ring_is_up}",
                (10, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Pinky : {hand.pinky_is_up}",
                (10, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

        # -----------------------------
        # Calculate Processing FPS
        # -----------------------------
        current_time = time.time()
        elapsed_time = current_time - prev_time

        if elapsed_time > 0:
            fps = 1 / elapsed_time
        else:
            fps = 0

        fps_history.append(fps)
        average_fps = sum(fps_history) / len(fps_history)

        prev_time = current_time

        cv2.putText(
            frame,
            f"Processing FPS: {average_fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # Display frame
        cv2.imshow("SignSpeak", frame)

        # Quit when Q is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()