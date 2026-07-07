"""
blank_hand_detector.py

Detects when a user has finished signing a letter.

A letter is committed only when:
1. A stable prediction exists.
2. The hand disappears after being visible.

This prevents the same letter from being added repeatedly while
the user continues holding the same sign.
"""


class BlankHandDetector:
    def __init__(self):
        """
        Initialize the detector.
        """
        self._hand_was_present = False
        self._last_prediction = None

    def update(self, hand_present: bool, stable_prediction: str | None):
        """
        Update the detector.

        Parameters
        ----------
        hand_present : bool
            True if a hand is currently detected.

        stable_prediction : str | None
            Stable prediction from PredictionStabilizer.
            None if no stable prediction exists.

        Returns
        -------
        str | None
            Returns the committed letter when the hand disappears.
            Otherwise returns None.
        """

        committed_letter = None

        if hand_present:
            self._hand_was_present = True

            # Remember the latest stable prediction while the hand is visible.
            if stable_prediction is not None:
                self._last_prediction = stable_prediction

        else:
            # Hand has just disappeared.
            if self._hand_was_present and self._last_prediction is not None:
                committed_letter = self._last_prediction

            # Reset for the next letter.
            self._hand_was_present = False
            self._last_prediction = None

        return committed_letter

    def reset(self):
        """
        Reset the detector state.
        """
        self._hand_was_present = False
        self._last_prediction = None