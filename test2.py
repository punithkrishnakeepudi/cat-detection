import cv2
from ultralytics import YOLO
from plyer import notification
import time
import smtplib
import ssl
from email.message import EmailMessage
import threading

# --- CONFIGURATION ---
EMAIL_SENDER = 'punithkrishna147@gmail.com'
EMAIL_PASSWORD = 'your_new_app_password'  # Paste your 16-char App Password here
EMAIL_RECEIVER = 'punithkrishna147@gmail.com'

# --- Global Variables ---
line_start = None
line_end = None
drawing = False
track_history = {}
notification_cooldown = 0


def send_email_alert():
    """
    Sends an email alert in a separate thread to avoid freezing the video.
    """
    subject = "ALERT: Cat Detected Crossing Line!"
    body = f"A cat was detected crossing your security line at {time.strftime('%H:%M:%S')}."

    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = EMAIL_RECEIVER
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, em.as_string())
        print(">> Email sent successfully.")
    except Exception as e:
        print(f">> Failed to send email: {e}")


def draw_line_callback(event, x, y, flags, param):
    global line_start, line_end, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        line_start = (x, y)
        line_end = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            line_end = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        line_end = (x, y)
        print(f"Line set: {line_start} to {line_end}")


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


# --- Main Setup ---
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
cv2.namedWindow("Cat Monitor")
cv2.setMouseCallback("Cat Monitor", draw_line_callback)

print("System Ready.")
print("1. Draw a line.")
print("2. If a cat crosses, you get an email.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model.track(frame, persist=True, classes=[15], verbose=False)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            current_pos = (float(x), float(y))

            if track_id in track_history:
                previous_pos = track_history[track_id]

                if line_start and line_end:
                    if intersect(previous_pos, current_pos, line_start, line_end):

                        # 10-second cooldown to avoid email spam
                        if (time.time() - notification_cooldown > 10):
                            print(f"!! Cat #{track_id} CROSSING DETECTED !!")

                            # 1. Desktop Notification
                            try:
                                notification.notify(
                                    title='Cat Alert',
                                    message='Sending email alert...',
                                    timeout=2
                                )
                            except:
                                pass

                            # 2. Send Email (In a background thread)
                            email_thread = threading.Thread(target=send_email_alert)
                            email_thread.start()

                            notification_cooldown = time.time()

                            # Visual Feedback
                            cv2.line(frame, line_start, line_end, (0, 0, 255), 5)

            track_history[track_id] = current_pos
            cv2.circle(frame, (int(current_pos[0]), int(current_pos[1])), 5, (0, 255, 0), -1)

        annotated_frame = results[0].plot()
    else:
        annotated_frame = frame

    if line_start and line_end:
        cv2.line(annotated_frame, line_start, line_end, (255, 0, 0), 2)

    cv2.imshow("Cat Monitor", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()