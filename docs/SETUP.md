# SignSpeak Development Setup

This document explains how to set up the development environment and run SignSpeak locally.

---

## Prerequisites

- Python 3.12+
- Git
- VS Code (recommended)

---

## Clone the Repository

```bash
git clone https://github.com/Royale-dev/SignSpeak.git
cd SignSpeak
```

---

## Create Virtual Environment

```powershell
python -m venv .venv
```

---

## Activate Virtual Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

### Git Bash

```bash
source .venv/Scripts/activate
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Run the Application

```powershell
python app/main.py
```

---

## Update Requirements

Whenever a new package is installed:

```powershell
pip freeze > requirements.txt
```

---

## Useful Git Commands

Check project status:

```bash
git status
```

Stage all changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "your message"
```

Push to GitHub:

```bash
git push
```

View commit history:

```bash
git log --oneline
```

---

## Project Structure

```
SignSpeak/
│
├── app/
│   ├── camera/
│   ├── vision/
│   ├── ml/
│   ├── speech/
│   ├── gui/
│   ├── utils/
│   └── main.py
│
├── assets/
├── datasets/
├── docs/
├── models/
├── tests/
│
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```