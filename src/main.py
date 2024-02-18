# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ritvik                                                       #
# 	Created:      1/15/2024, 12:03:14 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from tree import FruitColor, Orchard
from movement import *
from routes import *

# variable declaration
brain = Brain()

log = Log()

imu = Inertial(Ports.PORT20)
button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM
fruit_sonic = Sonar(brain.three_wire_port.a)
camera = Vision(Ports.PORT10, 43, FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT)

orchard = Orchard()

def activate_control():
	"""
	What the robot executes.
	"""
	while button.pressing():
		wait(5)
	drive(100, 0, 0)
	move_arm(5)
	move_claw(10)
	move_claw(0, stall=False)
	move_arm(0, stall=False)
	drive(-100, 0, 0)
	scan_fruit((0, 0))

def get_color() -> Signature:
	"""
	Finds a fruit and returns its color.

	Returns:
		Signature: the signature value of the color found.
	"""
	COLORS = [FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT]
	for color in COLORS:
		objects: Tuple[VisionObject] = camera.take_snapshot(color, 1)
		if objects:
			return color

	brain.screen.print_at("No fruit found.   ", x=50, y=100)
	raise Exception("Camera did not detect a fruit.")

def get_height() -> float:
	"""
	Returns the distance found by the ultrasonic sensor.

	Returns:
		float: the value returned by the sensors.
	"""
	height = fruit_sonic.distance(DistanceUnits.CM)
	if height > 20:
		raise Exception("Ultrasonic did not detect a fruit.")
	return height

def scan_fruit(location: tuple[int, int]) -> None:
	"""
	Calculates the color and height of the tree and adds it into the orchard at the given location.

	Params:
		location (tuple[int, int]): the location, (x, y) of the tree in a grid system.
	"""
	fruit_color: Signature = get_color()
	raw_height: float = get_height()
	orchard.add_tree(fruit_color, convert_height(raw_height), location)

def convert_height(old_height: float) -> float:
	"""
	Converts the raw ultrasonic sensor output to tree heights.

	Params:
		old_height (float): the raw value from the ultrasonic sensor.

	Returns:
		float: the tree height.
	"""
	return old_height

# initialize testing (will be triggered with button press and pre-run checks will be run here)
button.pressed(activate_control)
