# VS Wheel 🎮🏎️

**VS Wheel** is a camera-based virtual steering wheel system that uses hand gestures to control games through a virtual Xbox 360 controller.

Instead of using a physical steering wheel or gamepad, VS Wheel uses a webcam to track the user's hands and converts their movements and gestures into steering, throttle, and brake inputs.

## 🎯 Project Demo

VS Wheel has been successfully tested with a browser-based racing game.

The complete control pipeline works:

**Webcam → MediaPipe → Hand Gestures → VS Wheel → Virtual Xbox Controller → Racing Game**

## ✨ Features

* Hand tracking using MediaPipe
* Gesture-based analog steering
* Steering calibration
* Steering smoothing
* Adjustable steering sensitivity
* Right-hand thumb throttle control
* Left-hand thumb brake control
* Two-hand safety pause
* Virtual Xbox 360 controller using `vgamepad`
* Live steering dashboard
* Live throttle and brake indicators
* System status indicator
* Compatible with games that support Xbox-style controllers

## 🧠 How It Works

```text
Webcam
   ↓
MediaPipe Hand Tracking
   ↓
21 Hand Landmarks
   ↓
Gesture Detection
   ↓
Steering / Throttle / Brake
   ↓
Safety System
   ↓
Virtual Xbox 360 Controller
   ↓
Compatible Game
```

## 🎮 Controls

| Gesture / Key       | Action             |
| ------------------- | ------------------ |
| Hands rotated left  | Steer left         |
| Hands rotated right | Steer right        |
| Right thumb up      | Throttle           |
| Right thumb down    | Throttle off       |
| Left thumb down     | Brake              |
| Left thumb up       | Brake off          |
| Both hands open     | Safety pause       |
| `C` key             | Calibrate steering |
| `Q` key             | Quit               |

## 🖥️ Requirements

* Windows
* Python 3.12
* Webcam
* A game that supports Xbox-style controllers
* ViGEmBus-compatible virtual controller support

## 📦 Python Packages

VS Wheel uses:

* OpenCV
* MediaPipe
* vgamepad

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## 🤖 MediaPipe Model

VS Wheel requires the **MediaPipe Hand Landmarker** model.

Download the appropriate `hand_landmarker.task` model from the official MediaPipe documentation and place it here:

```text
models/hand_landmarker.task
```

The model file is intentionally not included in this repository.

## 🚀 Running VS Wheel

1. Clone the repository.

```bash
git clone <your-repository-url>
```

2. Open the project directory.

```bash
cd VSW
```

3. Create a Python virtual environment.

```bash
py -3.12 -m venv .venv
```

4. Activate the environment.

```powershell
.venv\Scripts\Activate.ps1
```

5. Install the required packages.

```bash
pip install -r requirements.txt
```

6. Make sure the MediaPipe model is located at:

```text
models/hand_landmarker.task
```

7. Run VS Wheel.

```bash
python main.py
```

## 🎯 Steering Calibration

Start VS Wheel and place your hands in your normal steering position.

Press:

```text
C
```

This sets the current hand position as the steering neutral position.

Move your hands left or right to control the virtual steering wheel.

## 🛡️ Safety System

VS Wheel includes a two-hand safety mechanism.

When both hands are detected as open:

```text
Steering = 0
Throttle = 0
Brake = 0
```

The virtual controller therefore stops sending driving input while the system is paused.

## 📁 Project Structure

```text
VSW/
│
├── models/
│   └── hand_landmarker.task
│
├── .gitignore
├── README.md
├── requirements.txt
├── controller_test.py
├── hand_tracking.py
└── main.py
```

## 🔬 Project Status

**VS Wheel 1.0 — Working Prototype**

The current version successfully demonstrates:

* Real-time hand tracking
* Gesture recognition
* Analog steering
* Throttle and brake control
* Safety pause
* Virtual Xbox controller output
* Real gameplay using the virtual controller

## 🛠️ Future Improvements

Possible future versions may include:

* Better hand-position calibration
* More advanced gesture recognition
* Automatic controller/game detection
* Improved performance
* Easier one-click startup
* Support for additional games
* Packaging VS Wheel as a standalone Windows application

## 📜 License

This project is currently published as a personal learning and demonstration project.
