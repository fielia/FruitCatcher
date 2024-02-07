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
right_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
drive_motors = MotorGroup(left_motor, right_motor)

arm_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)

button = Bumper(brain.three_wire_port.b)

ROBOT_IDLE = 0 
ROBOT_DETECTION = 1

state = ROBOT_IDLE

test_color = "LEMON"

def ButtonPress():
	global state
	global objects
	if(state == ROBOT_IDLE):
		brain.screen.print_at('IDLE -> DETECTION', x=50, y=50)
		state = ROBOT_DETECTION
		fruit_color = driveToFruit()
		# fruit_height = determineHeight(fruit_object)
		if not touchFruit(): # confirm motions were successful
			Exception("Arm Failed.")
		brain.screen.print_at("Touched the " + fruit_color, x=50, y=150)
	else:
		brain.screen.print_at('-> IDLE', x=50, y=50)
		left_motor.stop()
		right_motor.stop()
		state = ROBOT_IDLE

button.pressed(ButtonPress)

sleep(20)

# returns the objects of the fruit, and displays the color on the screen
def determineColor(color: str) -> Tuple[VisionObject, str]:
	objects: Tuple[VisionObject] = camera.take_snapshot(COLORS[COLOR_STRINGS.index(color)], 1)
	if objects:
		brain.screen.print_at("Color: " + color + ".     ", x=50, y=100)
		return (objects[0], color)

	brain.screen.print_at("No fruit found.   ", x=50, y=100)
	fake_object: VisionObject = VisionObject()
	return (fake_object, "null")

tolerance: float = 10
# returns the x and y distance away from the camera
def centerFruit() -> str: ## this code doesn't do anything with the objects here, but you could
	left_motor.set_velocity(50, RPM)
	right_motor.set_velocity(50, RPM)

	cx: float = 0
	global tolerance
	while True:
		fruit_object, fruit_color = determineColor(test_color)
		
		if not fruit_color == "null":
			cx = fruit_object.centerX - 158
		
		if fruit_color == "null":
			left_motor.stop()
			right_motor.stop()
			return fruit_color
		elif cx > tolerance:
			left_motor.spin(REVERSE)
			right_motor.spin(FORWARD)
		elif cx < -tolerance:
			left_motor.spin(FORWARD)
			right_motor.spin(REVERSE)
		else:
			left_motor.stop()
			right_motor.stop()
			return fruit_color

# NOTE: all measurements are in CM!

focal_length: float = 134.44 # F = D * P / W, or the focal length is the distance * pixels / actual width
CENTER: int = 0
DRIVE: int = 1

def foundObject(fruit_color: str) -> bool:
	if not fruit_color in COLOR_STRINGS:
		return False
	objects: Tuple[VisionObject] = camera.take_snapshot(COLORS[COLOR_STRINGS.index(fruit_color)], 1)
	if objects:
		brain.screen.print_at("Color: " + fruit_color + ".     ", x=50, y=100)
		return True
	brain.screen.print_at("No fruit found.   ", x=50, y=100)
	return False

def checkCentered(fruit_color: str) -> bool:
	if not fruit_color in COLOR_STRINGS:
		return False
	objects: Tuple[VisionObject] = camera.take_snapshot(COLORS[COLOR_STRINGS.index(fruit_color)], 1)
	if not objects:
		return False
	fruit_object: VisionObject = objects[0]
	cx: int = fruit_object.centerX - 158
	global tolerance
	
	if cx > tolerance or cx < -tolerance:
		return False
	return True

wheel_diameter: float = 10
def driveToFruit() -> str:
	drive_state = CENTER
	fruit_color = centerFruit()
	if not foundObject(fruit_color):
		drive_motors.spin_for(FORWARD, 540 * 2, DEGREES, 100, RPM)
	while foundObject(fruit_color):
		if drive_state == CENTER:
			brain.screen.print_at("Centering", x=50, y=150)
			centerFruit()
			brain.screen.print_at("Centered ", x=50, y=150)
			drive_state = DRIVE
		elif drive_state == DRIVE:
			drive_motors.spin(FORWARD, 100, RPM)
			if not foundObject(fruit_color):
				break
			wait(250)
			if not checkCentered(fruit_color):
				drive_state = CENTER
	return fruit_color

possible_heights: list[float] = [17, 29, 38]
def determineHeight(fruit_object: VisionObject) -> float: # not needed for these tests
	cy = fruit_object.height

	if cy > 0 and cy < 0: # TODO: set values
		return possible_heights[0]
	elif cy > 0 and cy < 0: # TODO: set values
		return possible_heights[1]
	elif cy > 0 and cy < 0: # TODO: set values
		return possible_heights[2]

	return 0

def touchFruit() -> bool: # currently not final product, merely temporary for test
	arm_motor.set_velocity(150, RPM)
	drive_motors.spin_for(REVERSE, 810, DEGREES)
	centerFruit()
	arm_motor.spin_for(FORWARD, 210 * 4, DEGREES)
	drive_motors.spin_for(FORWARD, 630, DEGREES)
	drive_motors.spin_for(REVERSE, 720, DEGREES)
	arm_motor.spin_for(REVERSE, 210 * 4, DEGREES)
	return True

camera_to_arm_base: float = 4.5 # the vertical distance from camera to arm base
arm_length: float = 21 # the length of the arm
