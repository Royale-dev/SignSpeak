"""
train_classifier.py
Train a landmark classifier for SignSpeak.
"""

from pathlib import Path
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "datasets" / "raw" / "landmarks.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(CSV_PATH)

X = df.drop(columns=["label"]).astype("float32").values
y = df["label"].values

print(f"Loaded {len(df)} samples.")

encoder = LabelEncoder()
y = encoder.fit_transform(y)

with open(MODEL_DIR / "label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

scaler = StandardScaler()
X = scaler.fit_transform(X)

with open(MODEL_DIR / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Sequential([
    Input(shape=(X.shape[1],)),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dropout(0.3),
    Dense(len(encoder.classes_), activation="softmax"),
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[
        EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True,
        )
    ],
)

pred = np.argmax(model.predict(X_test, verbose=0), axis=1)

print("\nAccuracy :", accuracy_score(y_test, pred))
print("Precision:", precision_score(y_test, pred, average="weighted"))
print("Recall   :", recall_score(y_test, pred, average="weighted"))
print("F1 Score :", f1_score(y_test, pred, average="weighted"))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print(classification_report(y_test, pred, target_names=encoder.classes_))

model.save(MODEL_DIR / "asl_classifier.keras")

plt.figure()
plt.plot(history.history["accuracy"], label="Train")
plt.plot(history.history["val_accuracy"], label="Validation")
plt.legend()
plt.title("Accuracy")
plt.show()

plt.figure()
plt.plot(history.history["loss"], label="Train")
plt.plot(history.history["val_loss"], label="Validation")
plt.legend()
plt.title("Loss")
plt.show()
