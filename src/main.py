# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ritvik                                                       #
# 	Created:      2/14/2024, 8:33:31 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from tree import FruitColor, Orchard
from movement import Log, drive, rotate, move_arm, move_claw, toggle_door, kill
from routes import go_to

# variable declaration
brain = Brain()

imu = Inertial(Ports.PORT20)
button = Bumper(brain.three_wire_port.a)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM
fruit_sonic = Sonar(brain.three_wire_port.c)
camera = Vision(Ports.PORT14, 43, FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT)

orchard = Orchard()

CLAW_CHOP_POSITION: float = 0 # position of the claw right after chopping a fruit

# start robot at the corner near the exit sign

def testing():
	brain.screen.clear_screen()
	go_to((0, 0))
	scan_fruit((0, 0))
	while True:
		kill()

def activate_auto():
	"""
	What the robot executes.
	"""
	global orchard
	while button.pressing():
		wait(5)
	current_tree: tuple[int, int] = (0, 0)
	go_to(current_tree)
	scan_fruit(current_tree)
	move_arm(orchard.get_tree_height(current_tree))
	move_claw(CLAW_CHOP_POSITION)
	move_claw(0, stall=False)
	move_arm(0, stall=False)
	Log.return_to_origin()

def _get_color() -> Signature:
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

def _get_height() -> float:
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
	fruit_color: Signature = _get_color()
	raw_height: float = _get_height()
	orchard.add_tree(fruit_color, _convert_height(raw_height), location)

def _convert_height(old_height: float) -> float:
	"""
	Converts the raw ultrasonic sensor output to tree heights (this value is the position the arm will be in to grab fruits).

	Params:
		old_height (float): the raw value from the ultrasonic sensor.

	Returns:
		float: the tree height.
	"""
	new_height: float = 0

	return new_height

# initialize testing (will be triggered with button press and pre-run checks will be run here)
imu.calibrate()
brain.screen.print_at("IMU Calibrating...", x=50, y=50)
while imu.is_calibrating():
	wait(100)
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)

button.pressed(testing)
