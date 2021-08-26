from djitellopy import tello
import cv2
from cvzone.FaceDetectionModule import FaceDetector

myDrone = tello.Tello()
myDrone.connect()
print(myDrone.get_battery())
myDrone.streamoff()
myDrone.streamon()

detector = FaceDetector(0.6)  # face detector using mediapipe libary

while True:
    img = myDrone.get_frame_read().frame
    cv2.resize(img, (640, 480))
    img, bbox = detector.findFaces(img, draw=True)  # bbox - bounding box
    cv2.imshow("Video",img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        myDrone.streamoff()
        break


cv2.destroyAllWindows()
