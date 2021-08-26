import cv2
from djitellopy import tello
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import cvzone
import time

# Webcam testing
# cap = cv2.VideoCapture(0)


DetectorFace = FaceDetector()
DetectorHand = HandDetector(maxHands=1)
gesture = ""

myDrone = tello.Tello()
myDrone.connect()
print(myDrone.get_battery())
myDrone.takeoff()
myDrone.move_up(80)

myDrone.streamoff()
myDrone.streamon()
# myDrone.move_up(40)
# myDrone.move("up", 60)
beginningTime = time.time()
myDrone.send_rc_control(0, 0, 0, 5)
while True:
    # Webcam testing
    # _, img = cap.read()
    img = myDrone.get_frame_read().frame  # drone frames
    if not img is None:
        img = cv2.resize(img, (640, 480))
        # ------------ HANDS ------------
        img = DetectorHand.findHands(img, draw=True)
        lmList, bboxHand = DetectorHand.findPosition(img, draw=False)
        # ------------ Face ------------
        img, bboxFace = DetectorFace.findFaces(img, draw=True)

        # ------------ Hands & Face ------------
        if bboxFace:
            x, y, h, w = bboxFace[0]["bbox"]
            bboxRegion = x - 175 - 50, y - 75, 175, h + 75
            cvzone.cornerRect(img, bboxRegion, rt=0, t=10, colorC=(0, 0, 255))
            # print(DetectorHand.handType())

            if bboxHand and DetectorHand.handType() == "Right":

                handCenter = bboxHand["center"]
                #           x         <     cx      <         x + width
                inside = bboxRegion[0] < handCenter[0] < bboxRegion[0] + bboxRegion[2] and \
                         bboxRegion[1] < handCenter[1] < bboxRegion[1] + bboxRegion[3]

                if inside:
                    cvzone.cornerRect(img, bboxRegion, rt=0, t=10, colorC=(0, 255, 0))

                    fingers = DetectorHand.fingersUp()
                    # print(fingers)
                    # thumb, index, middle, ring, pinky = DetectorHand.fingersUp()

                    # FIRST OPTION
                    # thumb, index, middle, ring, pinky = DetectorHand.fingersUp()
                    # if thumb and index and middle and ring and pinky:
                    #     print("Open Hand")
                    # elif not thumb and index and not middle and not ring and not pinky:
                    #     print("Index finger")

                    if fingers == [1, 1, 1, 1, 1]:
                        gesture = "  Stop"
                    elif fingers == [0, 1, 0, 0, 0]:
                        gesture = "  UP"
                        myDrone.move_up(20)
                    elif fingers == [0, 0, 0, 0, 0]:
                        gesture = "  Stop"
                    # elif fingers == [0, 0, 1, 0, 0]:
                    #   gesture = "  middle"
                    elif fingers == [1, 1, 0, 0, 1]:
                        gesture = "Flip"
                        myDrone.flip_back()
                    elif fingers == [0, 1, 1, 0, 0]:
                        gesture = " Down"
                        myDrone.move_down(20)

                    elif fingers == [0, 0, 0, 0, 1]:
                        gesture = "  Left"
                        myDrone.move_left(40)
                    elif fingers == [1, 0, 0, 0, 0]:
                        gesture = "  Right"
                        myDrone.move_right(40)

                    cv2.rectangle(img, (bboxRegion[0] + 10, bboxRegion[1] + bboxRegion[3] + 10),
                                  (bboxRegion[0] + bboxRegion[2], bboxRegion[1] + bboxRegion[3] + 60),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{gesture}', (bboxRegion[0] + 15, bboxRegion[1] + bboxRegion[3] + 50),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        cv2.resize(img,(1280,720))
        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        currtime = time.time()
        if currtime - beginningTime > 120:
            print("times up")
            myDrone.streamoff()
            myDrone.land()
            break
    time.sleep(0.02)

cv2.destroyAllWindows()
# cap.release()
