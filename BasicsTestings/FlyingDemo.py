from djitellopy import tello
import time

myDrone = tello.Tello()
myDrone.connect()

print(myDrone.get_battery())



myDrone.takeoff()

# Move using distance

# on the default height it doesnt recognize the person so we will lift it alittle bit
myDrone.move_up(30)  # x is Centimeters. alternative command is myDrone.move("up",50)

# Move using speed

# Command for the speed of the drone
myDrone.send_rc_control(0, 0, 0, 20)  # rotate to the opposite: myDrone.send_rc_control(0,0,0, -20 )
time.sleep(3)
myDrone.send_rc_control(0, 0, 0, 0)

myDrone.land()