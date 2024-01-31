# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       glewin                                                       #
# 	Created:      9/11/2023, 8:28:37 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

## define the colors; we'll use the default sensitivity of 3.0
## you don't have to retrain the camera to use different sensitivities; you can just change the value here # TODO: fix signatures
ORANGE_FRUIT = Signature(1, 4915, 6305, 5610, -2305, -1901, -2103, 3.0, 0)
LIME = Signature(2, -7385, -6527, -6956, -4551, -3459, -4005, 3.0, 0)
LEMON = Signature(3, 1907, 2409, 2158, -3619, -3129, -3374, 3.0, 0)
DRAGON_FRUIT = Signature(4, 0, 0, 0, 0, 0, 0, 3.0, 0,)

## define the camera on port 3; the library says the colors are optional -- you do you
Vision3 = Vision(Ports.PORT3, 72, ORANGE_FRUIT, LIME, LEMON, DRAGON_FRUIT)

brain.screen.print("Hello V5")

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1

## start in the idle state
state = ROBOT_IDLE

def handleButtonPress():
	global state
	if(state == ROBOT_IDLE):
		print('IDLE -> SEARCHING')
		state = ROBOT_SEARCHING
		left_motor.spin(FORWARD, 30)
		right_motor.spin(FORWARD, -30)

	else:
		print(' -> IDLE')
		left_motor.stop()
		right_motor.stop()

button5 = Bumper(Ports.PORT5)
button5.pressed(handleButtonPress)

def determineFruit(objects):
	return
def calculateDistance(objects, fruit_type): ## this code doesn't do anything with the objects here, but you could
	cx = Vision3.largest_object().centerX
	cy = Vision3.largest_object().centerY

	print(cx, cy)

while True:
	'''
	These lines correspond to a checker-handler: check for an object and handle it if there is one.
	'''
	objects = Vision3.take_snapshot(ORANGE_FRUIT)
	if objects:
		fruit_type = determineFruit(objects)
		calculateDistance(objects, fruit_type)


	## a little nap to not overwhelm the system -- the frame rate will be well under 50 Hz anyway
	sleep(20)
