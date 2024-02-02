# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       nicholaskruse                                                #
# 	Created:      1/30/2024, 12:47:11 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

sensitivity = 2

#Color Calibration
GRAPEFRUIT = Signature(1, 6513, 7443, 6978, 1111, 1431, 1271, sensitivity, 0)
LIME = Signature(2, -6249, -5385, -5817, -3721, -3023, -3372, sensitivity, 0)
LEMON = Signature(3, 2607, 3087, 2846, -3461, -3199, -3330, sensitivity, 0)
ORANGE_FRUIT = Signature(4, 7581, 8071, 7826, -2049, -1809, -1929, sensitivity, 0)
COLORS = [GRAPEFRUIT, LIME, LEMON, ORANGE_FRUIT]
COLOR_STRINGS = ["GRAPEFRUIT", "LIME", "LEMON", "ORANGE"]

#Vision Defined
camera = Vision(Ports.PORT10, 43, GRAPEFRUIT, LIME, LEMON, ORANGE_FRUIT)

left_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT21, GearSetting.RATIO_18_1, True)
arm_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)

button = Bumper(brain.three_wire_port.b)

ROBOT_IDLE = 0 
ROBOT_DETECTION = 1

state = ROBOT_IDLE

def testColor():
	brain.screen.clear_screen()
	determineColor()
	wait(200)
	brain.screen.print_at("Press again.", x=50, y=50)

button.pressed(testColor)

def ButtonPress():
	global state 
	global objects
	if(state == ROBOT_IDLE):
		brain.screen.print_at('IDLE -> DETECTION', x=50, y=50)
		state = ROBOT_DETECTION
		objects = determineColor()
		fruit_stats = determineFruit(objects[0])
		(distance_x, distance_y) = calculateDistance(objects[0], fruit_stats[0], fruit_stats[1])
		
	else:
		brain.screen.print_at('-> IDLE', x=50, y=50)
		left_motor.stop()
		right_motor.stop()


sleep(20)

# returns the objects of the fruit, and displays the color on the screen
def determineColor() -> Tuple[VisionObject]:
	for i in range(len(COLORS)):
		objects: Tuple[VisionObject] = camera.take_snapshot(COLORS[i], 1)
		if objects:
			brain.screen.print_at("Color: " + COLOR_STRINGS[i], x=50, y=100)
			return objects

	brain.screen.print_at("No fruit found.", x=50, y=100)
	exit(0)

# NOTE: all measurements are in MM!

fruit_length: int = 0
possible_widths = [5.5, 9]
possible_heights = [17, 29, 38]

# returns the width of the fruit (of 2 options) and height off the ground (of 3 options). length is defined below
def determineFruit(fruit_object: VisionObject) -> Tuple[int, int]:
	width = 0
	height = 0

	return (width, height)

# returns the x and y distance away from the camera
def calculateDistance(fruit_object: VisionObject, fruit_width: int, fruit_height: int) -> Tuple[int, int]: ## this code doesn't do anything with the objects here, but you could
	cx = fruit_object.centerX
	cy = fruit_object.centerY
	print(cx, cy)

	distance_x = 0
	distance_y = 0

	return (distance_x, distance_y)
