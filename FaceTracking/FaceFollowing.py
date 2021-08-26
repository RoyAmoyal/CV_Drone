from djitellopy import tello
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import cvzone
import numpy as np
import time

detector = FaceDetector(minDetectionCon=0.8)  # face detector using mediapipe libary
# WEBCAM TESTING
# cap = cv2.VideoCapture(0)
# _, img = cap.read()
# cv2.resize(img, (640, 480))
# height, width, _ = img.shape
## print(height, weight)

height, width = 480, 640

# P   I  D - controlling the speed of the drone (P), and stabilizing and drone (I,D). we set the P,D,I values with Tuning
# (watch comments bellow)
xPID = cvzone.PID([0.22, 0, 0.1], width // 2, axis=0)  # when we reduce the P val its called Tuning
yPID = cvzone.PID([0.25, 0, 0.1], height // 2, axis=1)  # when we reduce the P val its called Tuning
# IMPORTANT 0.003 IS SAFETY BECAUSE THE DRONE MIGHT HAVE NO TIME TO STOP WHEN IT MOVES
zPID = cvzone.PID([0.005, 0, 0.002], 12000,limit=[-20,15])

# FORWARD AND IT MIGHT HIT ME.
# 3000 value is taken from testing with webcam 640 x 480 like the tello camera.


# D - is resposible to reduce the speed of the drone when reaching the center to overcome the momentum.

# myPlotX = cvzone.LivePlot(w=1280, h=720, yLimit=[-(width // 2), width // 2], char='X')
# myPlotY = cvzone.LivePlot(w=1280, h=720, yLimit=[-(height // 2), height // 2], char='Y')
myPlotX = cvzone.LivePlot(w=1280, h=720, yLimit=[-100, 100], char='X')
myPlotY = cvzone.LivePlot(w=1280, h=720, yLimit=[-100, 100], char='Y')
myPlotZ = cvzone.LivePlot(w=1280, h=720, yLimit=[-100, 100], char='Z')

myDrone = tello.Tello()
myDrone.connect()
time.sleep(3)
myDrone.streamoff()
myDrone.streamon()
print(myDrone.get_battery())
myDrone.takeoff()

#myDrone.move_up(10)
#myDrone.move("up", 60)
beginningTime = time.time()

while True:
    img = myDrone.get_frame_read().frame  # drone frames
    img = cv2.resize(img, (640, 480))

    # webcam testing
    # _, img = cap.read() # webcam testing
    # cv2.resize(img, (640, 480))
    img, bbox = detector.findFaces(img, draw=True)  # bbox - bounding box

    # In case no face detected
    imgPlotX = np.zeros((height, width, 3), np.uint8)
    imgPlotY = np.zeros((height, width, 3), np.uint8)
    imgPlotZ = np.zeros((height, width, 3), np.uint8)
    xVal = 0
    yVal = 0
    zVal = 0

    if bbox:  # if the list isn't empty
        print("Face detected")
        cx, cy = bbox[0]['center']
        x, y, w, h = bbox[0]['bbox']  # ['bbox'] contain the information of the bounding box around the face
        area = w * h
        # print(area)
        xVal = int(xPID.update(cx))  # floating point Converted to int for the drone
        imgPlotX = myPlotX.update(xVal)

        yVal = int(yPID.update(cy))  # floating point Converted to int for the drone
        imgPlotY = myPlotY.update(yVal)

        zVal = int(zPID.update(area))
        # print(zVal)
        imgPlotZ = myPlotZ.update(zVal)

        # drawings
        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        # imgStacked = cvzone.stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
        #imgStacked = cvzone.stackImages([img, imgPlotX], 2, 0.75)
        imgStacked = cvzone.stackImages([img], 1, 1.5)
    else:
        imgStacked = cvzone.stackImages([img], 1, 1.5)

        # cv2.putText(img, str(xVal), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) # Px draw
        # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (width // 2, 0), (width // 2, height), (255, 0, 255), 1)
        # error = weight // 2 - cx
        # cv2.putText(img, str(error), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # cv2.line(img, (width // 2, height // 2), (cx, cy), (255, 0, 255), 2)

    # cv2.imshow("imgPlotX", imgPlotX)
    # imgStacked = cvzone.stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)

    # if there is - before xval,yval,zval is because the drone is moving the opposite way with the original values xval,yval,zval
    # myDrone.send_rc_control(0,zVal,yVal,xVal)

    # testings for tunings
    #Tuning X
    myDrone.send_rc_control(0, -zVal, -yVal, xVal)
    #Tuning Y
    #myDrone.send_rc_control(0, 0, yVal, 0)
    #Tuning Z
    #myDrone.send_rc_control(0, zVal, 0, 0)

    cv2.imshow("AllImages", imgStacked)
    # cv2.imshow("Video", img)
    if cv2.waitKey(3) & 0xFF == ord('q'):
        myDrone.streamoff()
        myDrone.land()
        break
    currtime = time.time()
    if currtime - beginningTime > 90:
        print("times up")
        myDrone.streamoff()
        myDrone.land()
        break

cv2.destroyAllWindows()
cv2.waitKey(2)
