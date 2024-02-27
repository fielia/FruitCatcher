from vex import *
from tree import FruitColor, Orchard
from movement import drive, drive_speed, move_arm, move_claw, brain

fruit_sonic = Sonar(brain.three_wire_port.c) # NOTE: has a range of 30 to 3000 MM
camera = Vision(Ports.PORT14, 70, FruitColor.LIME) #, FruitColor.LEMON, FruitColor.ORANGE_FRUIT)

orchard = Orchard()

CLAW_SQUEEZE: float = 90
CLAW_CHOP: float = 90 # position of the claw right after chopping a fruit
ARM_LOW: float = 125
ARM_MID: float = 1040
ARM_HIGH: float = 1925

def _get_color():
	"""
	Finds a fruit and returns its color.

	Returns:
		Signature: the signature value of the color found.
	"""
	COLORS = [FruitColor.LIME] #, FruitColor.ORANGE_FRUIT]
	for color in COLORS:
		objects: Tuple[VisionObject] = camera.take_snapshot(color, 1)
		if objects:
			return color

	brain.screen.print_at("No fruit found.   ", x=50, y=100)
	return 0 #Signature(0, 0, 0, 0, 0, 0, 0, 0, 0)
	# raise Exception("Camera did not detect a fruit.")

def _get_height() -> float:
	"""
	Returns the distance found by the ultrasonic sensor.

	Returns:
		float: the value returned by the sensors.
	"""
	return fruit_sonic.distance(DistanceUnits.MM)
	

def get_fruit(location: tuple[int, int]) -> None:
	"""
	Calculates the color and height of the tree and adds it into the orchard at the given location.

	Params:
		location (tuple[int, int]): the location, (x, y) of the tree in a grid system.
	"""
	if orchard.new_tree_discovered(location):
		sig = _get_color()
		if sig:
			fruit_color: Signature = sig
			_center_on_fruit(fruit_color)
			print("finished centering on fruit")
			drive(-10, 0)
			wait(500)
			raw_height: float = _get_height()
			brain.screen.print_at(_convert_height(raw_height), x=100, y=50)
			orchard.add_tree(fruit_color, _convert_height(raw_height), location)
			drive(-50, 130)
		else:
			print("no fruit found")
		#wait(500)
	else:
		_center_on_fruit(orchard.get_tree_color(location))
		drive(-90, 130)
	#wait(500)
	_grab_fruit(orchard.get_tree_height(location))

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
	elif old_height < 160:
		return ARM_MID
	elif old_height < 340:
		return ARM_HIGH

	return 0

def _center_on_fruit(fruit_color):
	cx: float = 40 # default value to enter the while
	cy: float = 40 # default value to enter the while
	# cx: horizontal, cy: vertical
	tolerance: float = 10
	while abs(cx) > tolerance or abs(cy) > tolerance:
		objects = camera.take_snapshot(fruit_color, 1)
		if not objects:
			brain.screen.clear_screen(Color.RED)
			# raise Exception("No Fruit Found")
			drive_speed(-0.1,-0.1)
		else:
			print(objects[0].width)
			brain.screen.clear_screen(Color.GREEN)
			fruit = objects[0]
			cx = fruit.centerX - 158 # subtract the center pixel value to shift to center equal 0
			cy = fruit.centerY - 106 # subtract the center pixel value to shift to center equal 0
			effort_x = cx * -0.2
			effort_y = cy * -0.2
			drive_speed(effort_y, effort_x)
	drive_speed(0,0)
	brain.screen.clear_screen(Color.BLUE)
	sleep(500)

def _grab_fruit(fruit_height: float):
	move_arm(fruit_height)
	move_claw(CLAW_CHOP)
	move_arm(10, stall=True)
	move_claw(10, stall=False)
