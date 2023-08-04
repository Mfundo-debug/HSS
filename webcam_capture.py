"""
Write a python script that captures video from my computer's webcame using OpenCV and displays it in a flask web application.
"""
import cv2
import numpy as np
from flask import Flask, render_template, Response
import datetime
import smtplib
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, ALERT_RECIPIENTS, MOTION_THRESHOLD, VIDEO_FILENAME
 
#set up video recording parameters
video_filename = 'video.mp4v'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640,480))

app = Flask(__name__, template_folder='templates')
#Initialize the video capture object
cap = cv2.VideoCapture(0)
#Initialize the face recognizer object
motion_detected = False
motion_start_time = None
alert_sent = False
#define the motion detection function

def detect_motion(frame):
    global motion_detected, motion_start_time
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    if motion_start_time is None:
        motion_start_time = datetime.datetime.now()
    else:
        time_elapsed = datetime.datetime.now() - motion_start_time
        if time_elapsed.total_seconds() > 5:
            motion_start_time = None
            motion_detected = False
            alert_sent = False
    if motion_detected:
        return
    frame_delta = cv2.absdiff(gray, cv2.GaussianBlur(gray.copy(), (21,21), 0))
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations = 2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < motion_threshold:
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

        #send email alert
        if not alert_sent:
            message = 'Motion detected at {}'.format(datetime.datetime.now())
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, smtp_username, message)
            server.quit()
            alert_sent = True
        video_out.write(frame)
        break
    return frame

#Define the video capture function
def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        detect_motion(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#define the flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
#release the webcame and close all window when the flask app is shutdown 
def release_webcam():
    cap.release()
    cv2.destroyAllWindows()

import atexit
atexit.register(release_webcam)