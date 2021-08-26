import cv2
from cvzone.HandTrackingModule import HandDetector




cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)


while True:
    _, img = cap.read()
    img, bbox = detector.findFaces(img, draw=True)  # bbox - bounding box
    img = detector.findHands(img,draw=True)
    cv2.imshow("Video",img)
    cv2.waitKey(1)

    lmList, bboxInfo = detector.findPosition(img,draw=True)




