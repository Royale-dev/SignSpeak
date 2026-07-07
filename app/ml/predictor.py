
"""
predictor.py

Reusable inference engine for SignSpeak.
"""

from pathlib import Path
import pickle
import numpy as np
import tensorflow as tf


class Predictor:
    """Loads the trained model and performs inference."""

    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        model_dir = project_root / "models"

        self.model = tf.keras.models.load_model(
            model_dir / "asl_classifier.keras"
        )

        with open(model_dir / "scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        with open(model_dir / "label_encoder.pkl", "rb") as f:
            self.encoder = pickle.load(f)

        print("Predictor loaded successfully.")

    def preprocess(self, landmarks):
        """
        Accepts:
            - Hand object
            - MediaPipe landmark list
            - numpy array (63,)
        """

        # Our custom Hand class
        if hasattr(landmarks, "landmarks"):
            landmarks = landmarks.landmarks

        # MediaPipe landmark list
        if (
            hasattr(landmarks, "__len__")
            and len(landmarks) == 21
            and hasattr(landmarks[0], "x")
        ):
            features = []

            for lm in landmarks:
                features.extend([
                    lm.x,
                    lm.y,
                    lm.z,
                ])

            x = np.asarray(features, dtype=np.float32)

        else:
            x = np.asarray(
                landmarks,
                dtype=np.float32,
            ).flatten()

        if x.size != 63:
            raise ValueError(
                f"Expected 63 features, got {x.size}"
            )

        return self.scaler.transform(
            x.reshape(1, -1)
        )

    def predict(self, landmarks):
        x = self.preprocess(landmarks)

        probs = self.model.predict(x, verbose=0)[0]
        idx = int(np.argmax(probs))

        label = self.encoder.inverse_transform([idx])[0]
        confidence = float(probs[idx]) * 100.0

        return label, confidence

    def predict_from_array(self, array63):
        return self.predict(array63)
