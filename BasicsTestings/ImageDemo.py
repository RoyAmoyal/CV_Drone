from djitellopy import tello
import cv2

myDrone = tello.Tello()
myDrone.connect()
print(myDrone.get_battery())
myDrone.streamoff()
myDrone.streamon()

while True:
    img = myDrone.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Tello live video", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):  # sometimes waitKey(1) has issues with the tello so better use 5 miliseconds.
        myDrone.streamoff()
        break

cv2.destroyAllWindows()
