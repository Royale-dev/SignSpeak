"""
hand.py

Represents one detected hand.
"""


class Hand:
    """
    Represents a single detected hand.
    """

    def __init__(self, label, confidence, landmarks):
        self.label = label
        self.confidence = confidence
        self.landmarks = landmarks

    # -----------------------------
    # Landmark Properties
    # -----------------------------

    @property
    def wrist(self):
        return self.landmarks.landmark[0]

    @property
    def thumb_tip(self):
        return self.landmarks.landmark[4]

    @property
    def thumb_ip(self):
        return self.landmarks.landmark[3]

    @property
    def index_mcp(self):
        return self.landmarks.landmark[5]

    @property
    def index_tip(self):
        return self.landmarks.landmark[8]

    @property
    def middle_mcp(self):
        return self.landmarks.landmark[9]

    @property
    def middle_tip(self):
        return self.landmarks.landmark[12]

    @property
    def ring_mcp(self):
        return self.landmarks.landmark[13]

    @property
    def ring_tip(self):
        return self.landmarks.landmark[16]

    @property
    def pinky_mcp(self):
        return self.landmarks.landmark[17]

    @property
    def pinky_tip(self):
        return self.landmarks.landmark[20]

    # -----------------------------
    # Finger State Properties
    # -----------------------------

    @property
    def index_is_up(self):
        """
        Returns True if the index finger is raised.
        """
        return self.index_tip.y < self.index_mcp.y

    @property
    def middle_is_up(self):
        """
        Returns True if the middle finger is raised.
        """
        return self.middle_tip.y < self.middle_mcp.y

    @property
    def ring_is_up(self):
        """
        Returns True if the ring finger is raised.
        """
        return self.ring_tip.y < self.ring_mcp.y

    @property
    def pinky_is_up(self):
        """
        Returns True if the pinky finger is raised.
        """
        return self.pinky_tip.y < self.pinky_mcp.y