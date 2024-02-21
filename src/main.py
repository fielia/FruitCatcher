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
from movement import Log, drive, drive_speed, rotate, move_arm, move_claw, toggle_squeeze, toggle_door, kill, reset_motors, controller
from routes import go_to

# variable declaration
brain = Brain()

imu = Inertial(Ports.PORT20)
fruit_sonic = Sonar(brain.three_wire_port.c) # NOTE: has a range of 30 to 3000 MM
camera = Vision(Ports.PORT14, 43, FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT)

orchard = Orchard()

CLAW_SQUEEZE: float = 90
CLAW_CHOP: float = 115 # position of the claw right after chopping a fruit
ARM_LOW: float = 125
ARM_MID: float = 1040
ARM_HIGH: float = 1925

def testing():
	brain.screen.clear_screen()
	drive(0, 270)
	wait(100)
	drive(-600, 0)
	wait(500)
	drive(-50, 0)
	wait(500)
	scan_fruit((0, 0))
	drive(15, -25)
	brain.screen.print_at(orchard.get_tree_height((0, 0)), x=50, y=50)
	move_arm(orchard.get_tree_height((0, 0)))
	move_claw(CLAW_CHOP)
	move_arm(10, stall=False)
	move_claw(5)
	brain.screen.print_at("Done.", x=50, y=100)

def activate_auto():
	"""
	What the robot executes.
	"""
	while controller.buttonA.pressing():
		wait(5)
	current_tree: tuple[int, int] = (0, 0)
	go_to(current_tree)
	scan_fruit(current_tree)
	grab_fruit(orchard.get_tree_height(current_tree))
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
	return Signature(0, 0, 0, 0, 0, 0, 0, 0, 0)
	# raise Exception("Camera did not detect a fruit.")

def _get_height() -> float:
	"""
	Returns the distance found by the ultrasonic sensor.

	Returns:
		float: the value returned by the sensors.
	"""
	return fruit_sonic.distance(DistanceUnits.MM)
	

def scan_fruit(location: tuple[int, int]) -> None:
	"""
	Calculates the color and height of the tree and adds it into the orchard at the given location.

	Params:
		location (tuple[int, int]): the location, (x, y) of the tree in a grid system.
	"""
	fruit_color: Signature = _get_color()
	raw_height: float = _get_height()
	brain.screen.print_at(_convert_height(raw_height), x=100, y=50)
	orchard.add_tree(fruit_color, _convert_height(raw_height), location)

def _convert_height(old_height: float) -> float:
	"""
	Converts the MM ultrasonic sensor output to tree heights (this value is the position the arm will be in to grab fruits).

	Params:
		old_height (float): the MM value from the ultrasonic sensor.

	Returns:
		float: the tree height.
	"""

	if old_height < 70 or old_height > 3000:
		return ARM_LOW
	elif old_height < 150:
		return ARM_MID
	elif old_height < 340:
		return ARM_HIGH

	return 0

def center_on_fruit(fruit_color):
	cx: float = 10 # default value to enter the while
	cy: float = 10 # default value to enter the while
	# cx: horizontal, cy: vertical
	tolerance: float = 5
	while cx < tolerance and cy < tolerance:
		objects = camera.take_snapshot(fruit_color, 1)
		fruit = objects[0]
		cx = fruit.centerX - 50 # subtract the center pixel value to shift to center equal 0
		cy = fruit.centerY - 50 # subtract the center pixel value to shift to center equal 0
		effort_x = cx * 0.5
		effort_y = cy * 0.5
		drive_speed(effort_y, effort_x)

def grab_fruit(fruit_height: float):
	move_arm(fruit_height)
	move_claw(CLAW_CHOP)
	move_claw(10, stall=False)
	move_arm(10, stall=True)


# initialize testing (will be triggered with button press and pre-run checks will be run here)
imu.calibrate()
brain.screen.print_at("IMU Calibrating...", x=50, y=50)
while imu.is_calibrating():
	wait(100)
reset_motors()
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)

controller.buttonA.pressed(activate_auto)
