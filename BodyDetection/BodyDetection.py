from djitellopy import tello
import cv2
from cvzone.PoseModule import PoseDetector

detector = PoseDetector(upBody=True)
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    img = detector.findPose(img, draw=True)
    lmList, bboxInfo = detector.findPosition(img, draw=True)  # lmList - the landmarks on the body ,
    # bboxInfo = {"bbox": bbox, "center": (cx, cy)}

    cv2.imshow("Video", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):  # sometimes waitKey(1) has issues with the tello so better use 5 miliseconds.
        myDrone.streamoff()
        break

# cv2.destroyAllWindows()
