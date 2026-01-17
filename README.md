🐾 Cat Crossing Monitor (YOLOv8 + OpenCV)

A real-time computer vision application that detects cats and triggers desktop and email notifications if they cross a user-defined custom boundary.

✨ Features

Real-time Detection: Uses YOLOv8 (Nano) for high-speed cat detection.

Custom Boundary: Draw your own detection line directly on the video feed using your mouse.

Intelligent Tracking: Uses object tracking IDs to ensure notifications only trigger when the cat physically moves across the line.

Dual Notifications: * Native Desktop Pop-ups (via plyer).

Email Alerts with timestamps (via smtplib).

Threaded Alerts: Email sending happens in the background to prevent the video feed from lagging.

🛠️ Prerequisites

Python 3.8+

Webcam or video input device.

Gmail App Password: To send emails, you must use a Google "App Password" (not your standard login password).

🚀 Installation

Clone or Download this repository to your local machine.

Install the required libraries:

```bash
pip install ultralytics opencv-python plyer
```

📧 Email Configuration

Before running the script, open the Python file and update the CONFIGURATION section:

```python
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 16-character Google App Password
EMAIL_RECEIVER = 'target_email@gmail.com'
```

Note: To get an App Password, go to your Google Account Security settings, enable 2-Step Verification, and search for "App Passwords."

🎮 How to Use

Run the script:

```bash
python cat_monitor.py
```

Draw the Line: * Click and drag your left mouse button anywhere on the video window to draw your boundary line.

The line will appear in blue.

Detection:

The system will only look for cats (ignoring people, dogs, etc.).

When a cat's center point crosses the blue line, the line will momentarily flash red.

Controls:

Press 'c' to clear the current line and draw a new one.

Press 'q' to quit the application.

📈 Technical Details

The script uses a Line Segment Intersection algorithm. It calculates if the vector created by the cat's movement (Position A to Position B) intersects with the vector of your custom drawn line. This is significantly more accurate than simple coordinate boundary checks.

⚖️ License

This project is open-source and available under the MIT License.
# cat-detection

Lightweight cat detection and alert system using YOLOv8.

## Overview

This project uses a YOLOv8 model to detect and track cats from a webcam. Draw a line on the video window; if a detected cat crosses that line the script will notify you with a desktop notification and send an email alert (sent in a background thread).

Key file:
- `test2.py` — main script that loads `yolov8n.pt`, captures webcam frames, lets you draw a line, and alerts when a cat (COCO class id 15) crosses the line.

## Requirements

- Python 3.8+
- Packages: `ultralytics`, `opencv-python`, `plyer` (for desktop notifications). The `ultralytics` package requires a compatible `torch` installation.

Install (example):

```bash
pip install ultralytics opencv-python plyer
# Install torch according to your platform from https://pytorch.org/
```

Place the `yolov8n.pt` model file in the same folder (already included in this repo).

## Configuration

Open `test2.py` and set your email details near the top:

- `EMAIL_SENDER`
- `EMAIL_PASSWORD` (use a Gmail App Password; do NOT commit real credentials to the repository)
- `EMAIL_RECEIVER`

Security note: avoid committing credentials. Prefer reading the password from an environment variable or a separate, gitignored config file.

## Usage

1. Run the script:

```bash
python test2.py
```

2. A window named "Cat Monitor" will open:
- Click and drag to draw a line (left mouse button). The line is used as the crossing trigger.
- If a tracked cat crosses the line you'll see a desktop notification and an email is sent (background thread).
- Press `q` to quit.

## How it works (brief)

- Loads YOLOv8 model `yolov8n.pt` and runs tracking with `model.track(..., classes=[15])` to focus on cats.
- Tracks object positions across frames and checks segment intersection between object motion and the user-drawn line.
- On crossing, sends a desktop notification and triggers an email-sending thread with a 10-second cooldown to avoid spam.


## License

This repo is provided as-is. Add a license if you plan to publish publicly.
