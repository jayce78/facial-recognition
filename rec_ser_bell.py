import cv2
import numpy as np
import os
import time
import RPi.GPIO as GPIO
from PIL import Image, ImageTk

# Setup Servo PWM pin
servoPIN = 18

# Define GPIO numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO I/O Setup
GPIO.setup(servoPIN, GPIO.OUT)

# Servo and PWM setup
p = GPIO.PWM(servoPIN, 50) # setup with 50hz
p.start(2.5) # Set starting position

# Recognition and path links
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Facerec_project/trainer/trainer.yml')
cascadePath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Jason', 'Pernille', 'Nicholas', 'Sebastian', 'None4']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# Define servo movements
def servomovement():
	p.ChangeDutyCycle(5)
	time.sleep(0.5)
	p.ChangeDutyCycle(7.5)
	time.sleep(0.5)
	p.ChangeDutyCycle(10)
	time.sleep(0.5)
	p.ChangeDutyCycle(12.5)
	time.sleep(8)
	p.ChangeDutyCycle(10)
	time.sleep(0.5)
	p.ChangeDutyCycle(7.5)
	time.sleep(0.5)
	p.ChangeDutyCycle(5)
	time.sleep(0.5)
	p.ChangeDutyCycle(2.5)
	time.sleep(10)
	p.stop
	GPIO.cleanup()

while True:

    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    p.ChangeDutyCycle(0)
    time.sleep(0.5)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            print ("I SEE YOU", id)
            servomovement()

        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            print ("Unknown face detected")
            import doorbell.py

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

    cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()



