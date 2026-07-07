"""
live_test.py

Real-time webcam test for SignSpeak classifier.
"""

from pathlib import Path
import pickle
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL = tf.keras.models.load_model(PROJECT_ROOT/"models"/"asl_classifier.keras")

with open(PROJECT_ROOT/"models"/"scaler.pkl","rb") as f:
    SCALER = pickle.load(f)

with open(PROJECT_ROOT/"models"/"label_encoder.pkl","rb") as f:
    ENCODER = pickle.load(f)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam.")

prev = cv2.getTickCount()

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    text="No Hand"
    conf=0.0

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        feat=[]
        for lm in hand.landmark:
            feat.extend([lm.x,lm.y,lm.z])

        x = np.array(feat,dtype=np.float32).reshape(1,-1)
        x = SCALER.transform(x)

        probs = MODEL.predict(x,verbose=0)[0]
        idx = int(np.argmax(probs))
        text = ENCODER.inverse_transform([idx])[0]
        conf = float(probs[idx])*100

    now = cv2.getTickCount()
    fps = cv2.getTickFrequency()/(now-prev)
    prev = now

    cv2.putText(frame,f"Prediction: {text}",(20,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(frame,f"Confidence: {conf:.2f}%",(20,80),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)
    cv2.putText(frame,f"FPS: {fps:.1f}",(20,120),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)
    cv2.putText(frame,"ESC to quit",(20,160),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    cv2.imshow("SignSpeak Live Test",frame)

    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
