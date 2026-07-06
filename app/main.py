"""
main.py

Entry point for the SignSpeak application.
"""

import cv2
import time
from collections import deque

from camera.camera import Camera


def main():
    """
    Starts the SignSpeak application.
    """

    camera = Camera()

    # Used to calculate FPS
    prev_time = time.time()

    # Store the last 30 FPS values
    fps_history = deque(maxlen=30)

    while True:

        # Capture one frame
        frame = camera.get_frame()

        # Calculate FPS
        current_time = time.time()
        elapsed_time = current_time - prev_time

        # Prevent division by zero
        if elapsed_time > 0:
            fps = 1 / elapsed_time
        else:
            fps = 0

        # Save FPS in history
        fps_history.append(fps)

        # Calculate average FPS
        average_fps = sum(fps_history) / len(fps_history)

        # Prepare for next iteration
        prev_time = current_time

        # Draw FPS on the frame
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