#Mengyuan Wang 300256068
#Yufei Wang 300217244


from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import pygame 
import time
import dlib
import cv2
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from twilio.rest import Client
import json
from flask import Flask, request
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask import Flask, render_template, request


#This function calculates and return the ratio of eye aspect 
def ratio_eye(eye):

    distance_1 = np.sqrt(np.dot(eye[1]-eye[5],eye[1]-eye[5]))
    distance_2 = np.sqrt(np.dot(eye[2]-eye[4],eye[2]-eye[4]))
    distance_3 = np.sqrt(np.dot(eye[0]-eye[3],eye[0]-eye[3]))

    result = (distance_1+distance_2) / (2*distance_3)
    return result
    
#Calculate aspect ratio of both eyes
def both_eyes_ratio(left_eye,right_eye):

    left_eye_ratio = ratio_eye(left_eye)
    right_eye_ratio = ratio_eye(right_eye)

    both_eyes_ratio = (left_eye_ratio + right_eye_ratio) / 2
    return both_eyes_ratio
    
#Using convex hull to remove convex contour discrepencies and draw eye shape around eyes
def draw_eye_shape(left_eye,right_eye,frame):

    left_eye_convexhull = cv2.convexHull(left_eye)
    right_eye_convexhull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [left_eye_convexhull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [right_eye_convexhull], -1, (0, 255, 0), 1)

def video():


    #Initialize Pygame and load music
    #duration = 1000  # millisecond
    #freq = 1440  # Hz
    #winsound.Beep(freq, duration)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('audio/alert.mp3')

    #Setting the minimum threshold of eye aspect ratio below which alarm is triggerd
    eye_ratio_alarm_trigger = 0.26
    #Setting the minimum number of count that alarm will be triggered
    consecutive_count_alarm_trigger = 120
    #Setting the initial number of count
    COUNTER = 0





    #Load face cascade which will be used to draw a rectangle around detected faces.
    face_contour = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")


    #Load face detector and predictor, uses dlib shape predictor file
    face_detector = dlib.get_frontal_face_detector()


    #Loading the landmark detector
    face_landmark = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


    #Extract indexes of facial landmarks for the left and right eye
    (left_start, left_end) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    (right_start, right_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']


    #Turning on the camera
    cap = cv2.VideoCapture(0)
    freq = cv2.getTickFrequency() #the frequence of system


    #Give some time for camera to initialize
    time.sleep(2)


    while(True):
        #Read each frame and flip it
        success, frame = cap.read()
        frame = cv2.flip(frame,1)
        
        # convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect facial area
        face_area = face_detector(gray, 0)
        
        #Detect faces through haarcascade_frontalface_default.xml
        around_face_rectangle = face_contour.detectMultiScale(gray, 1.3, 5)
        
        #Draw rectangle around each face detected
        for (x,y,w,h) in around_face_rectangle:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        #Detect facial points
        for point in face_area:
            
            #detecting all landmarks 
            landmarks = face_landmark(gray, point)
            landmarks = face_utils.shape_to_np(landmarks)

            #Get array of coordinates of left eye and right eye
            left_eye = landmarks[left_start:left_end]
            right_eye = landmarks[right_start:right_end]
            draw_eye_shape(left_eye,right_eye,frame)
            tester_eye_ratio = both_eyes_ratio(left_eye,right_eye)

            #Detect if eye aspect ratio is less than threshold
            if(tester_eye_ratio < eye_ratio_alarm_trigger):
                COUNTER += 1
                print(COUNTER)
                #If the number of count is greater than the minimum number of count that the alarm will be trigger
                if COUNTER >= consecutive_count_alarm_trigger:
                    pygame.mixer.music.play()
                    cv2.putText(frame, "keep awake please!", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
                    # pygame.mixer.music.stop()


                    # sending message and making a call
                    account_sid = "AC8449f22835f51f278ecd27d05b987035"
                    auth_token = "cca822079f7efa34443acbfb9ccc316c"
                    client = Client(account_sid, auth_token)

                    # making a call
                    call = client.calls.create(to="16138696916",
                                               from_="+12566703018",
                                               url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")

            else:
                COUNTER = 0


        #Show video feed
        cv2.imshow('Video', frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break


# introduce Flask architecture
app = Flask(__name__)


# the method of exchange data with the front end
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        team_image = request.form.get("image")
        print(team_image)
        result='1'
        if team_image=='0':
            print(2222)
            video()
        return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=False)


