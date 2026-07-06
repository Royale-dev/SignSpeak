# SignSpeak Development Notes

## Project Vision

SignSpeak aims to be a professional desktop application capable of translating sign language into text and speech in real time.

The objective is not only to build an accurate machine learning model, but to create a polished, usable software product that demonstrates software engineering, computer vision, and machine learning skills.

---

## Design Goals

- Modular architecture
- Real-time performance
- Professional desktop interface
- Clean, maintainable code
- Easy future expansion

---

## Planned Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Computer Vision | OpenCV |
| Hand Detection | MediaPipe |
| Machine Learning | To be decided (PyTorch or TensorFlow) |
| GUI | PySide6 |
| Text-to-Speech | pyttsx3 |
| Version Control | Git & GitHub |

---

## Planned Architecture

```
Camera
   │
   ▼
OpenCV
   │
   ▼
MediaPipe Hand Detection
   │
   ▼
Hand Landmark Extraction
   │
   ▼
Gesture Recognition Model
   │
   ▼
Sentence Builder
   │
   ▼
Text-to-Speech
   │
   ▼
Desktop GUI
```

---

## Development Principles

- Understand every library before using it.
- Build one feature at a time.
- Make frequent Git commits.
- Write clean and documented code.
- Prefer maintainability over shortcuts.

---

## Current Status

Sprint 0 completed.

Next milestone:
- Webcam integration using OpenCV.