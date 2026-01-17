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
