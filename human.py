# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:57:44 2019
@author: seraj
"""
import time
import cv2
from flask import Flask, render_template, Response
import imutils
import numpy as np
import argparse
app = Flask(__name__)
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/camera1')
def camera1():
    """Video streaming home page."""
    return render_template('camera1.html')

@app.route('/camera2')
def camera2():
    """Video streaming home page."""
    return render_template('camera2.html')


def detect(frame):
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    for x, y, w, h in bounding_box_cordinates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, 'person {' + str(person) + '}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1

    cv2.putText(frame, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, 'Total Persons : {' + str(person - 1) + '}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0),
                2)
    cv2.imshow('output', frame)

    return frame
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def gen1():
    writer = None
    print('[INFO] Opening Video from path.')
    video = cv2.VideoCapture('2.mp4')
    #video = cv2.VideoCapture('http://192.168.0.5:8090/?action=stream')
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        # check is True if reading was successful
        check, frame = video.read()

        if check:
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            frame = detect(frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            break
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'

def gen2():
    writer2 = None
    print('[INFO] Opening Video from path.')
    video2 = cv2.VideoCapture('1.mp4')
    check2, frame2 = video2.read()
    if check2 == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video2.isOpened():
        # check is True if reading was successful
        check2, frame2 = video2.read()

        if check2:
            frame2 = imutils.resize(frame2, width=min(800, frame2.shape[1]))
            frame2 = detect(frame2)

            if writer2 is not None:
                writer2.write(frame2)

            key2 = cv2.waitKey(1)
            if key2 == ord('q'):
                break
        else:
            break
        image2 = cv2.imencode('.jpg', frame2)[1].tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image2 + b'\r\n'



@app.route('/video_feed1')
def video_feed1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen1(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen2(),mimetype='multipart/x-mixed-replace; boundary=frame')