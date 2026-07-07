"""
prediction_stabilizer.py

Smooths live predictions using a majority vote over
the last N predictions.
"""

from collections import deque, Counter


class PredictionStabilizer:
    """
    Stabilizes noisy predictions from the classifier.

    Example
    -------
    A A A B A A A A

    -> Stable prediction: A
    """

    def __init__(self, window_size=10, threshold=8):
        """
        Parameters
        ----------
        window_size : int
            Number of recent predictions to remember.

        threshold : int
            Minimum votes required before accepting
            a prediction as stable.
        """

        self.window_size = window_size
        self.threshold = threshold

        self.history = deque(maxlen=window_size)

        self.stable_prediction = None

    def reset(self):
        """
        Clears prediction history.
        """

        self.history.clear()
        self.stable_prediction = None

    def update(self, prediction):
        """
        Adds a new prediction and returns the current
        stable prediction.

        Parameters
        ----------
        prediction : str

        Returns
        -------
        str or None
        """

        self.history.append(prediction)

        counts = Counter(self.history)

        label, votes = counts.most_common(1)[0]

        if votes >= self.threshold:
            self.stable_prediction = label

        return self.stable_prediction

    @property
    def current_prediction(self):
        """
        Most recent prediction.
        """

        if not self.history:
            return None

        return self.history[-1]

    @property
    def current_votes(self):
        """
        Number of votes for the most common prediction.
        """

        if not self.history:
            return 0

        counts = Counter(self.history)

        return counts.most_common(1)[0][1]