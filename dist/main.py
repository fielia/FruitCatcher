# Packed by compile.py
from io import StringIO
from sys import print_exception
from re import match
from sys import exit


__ModuleCache__ = {}

class __ModuleNamespace__():
	def __init__(self, kwargs):
		for name in kwargs:
			setattr(self, name, kwargs[name])

	def __contains__(self, key):
		return key in self.__dict__

	def __iter__(self):
		return self.__dict__.__iter__()

def __define__src_tree():
	if "src_tree" in __ModuleCache__: return __ModuleCache__["src_tree"]
	__name__ = "__src_tree__"
	from vex import *
	
	class FruitColor():
		"""
		An enum to better access the colors.
	
		Params:
			_sensitivity (float): the sensitivity value for each color.
		"""
		_sensitivity: float = 2
		GRAPEFRUIT = Signature(1, 6513, 7443, 6978, 1111, 1431, 1271, _sensitivity, 0)
		LIME = Signature(2, -6249, -5385, -5817, -3721, -3023, -3372, _sensitivity, 0)
		LEMON = Signature(3, 2607, 3087, 2846, -3461, -3199, -3330, _sensitivity, 0)
		ORANGE_FRUIT = Signature(4, 7581, 8071, 7826, -2049, -1809, -1929, _sensitivity, 0)		
	
	possible_heights: list[float] = [17, 29, 38]
	class Tree():
		"""
		Represents one tree on the field.
	 
		Params:
			_fruit_color (Signature): the color of the fruits on the tree.
			_height (float): the height of the branches on the tree.
			_num_picked (int): the amount of fruit picked (starts at 0, maxes out at 4).
		"""
		_fruit_color: Signature
		_height: float
		_num_picked: int
	
		def __init__(self, fruit_color: Signature, height: float) -> None:
			self._fruit_color = fruit_color
			self._height = height
			self._num_picked = 0
		
		def get_fruit_color(self) -> Signature:
			return self._fruit_color
		
		def get_height(self) -> float:
			return self._height
		
		def picked_one(self) -> None:
			self._num_picked += 1
	
		def get_picked(self) -> int:
			return self._num_picked
	
	class Orchard():
		"""
		Represents the orchard, and contains all the trees.
	
		Params:
			_trees (List[List[Tree]]): a 2D array of the trees.
		"""
		_trees: List[List[Tree]]
	
		def __init__(self) -> None:
			self._trees = [[], [], []]
	
		def _at_location(self, location: tuple[int, int]):
			return self._trees[location[0]][location[1]]
		
		def new_tree_discovered(self, location: tuple[int, int]) -> bool:
			"""
			Checks if a tree in a given location has been logged.
	
			Params:
				location (tuple[int, int]): the location of the tree to check.
	
			Returns:
				bool: true if a tree is not found at the location, false otherwise.
			"""
			return not self._at_location(location)
	
		def add_tree(self, color: Signature, height: float, location: tuple[int, int]) -> bool:
			"""
			Adds a tree to the orchard, if the tree has not already been logged.
	
			Params:
				color (Signature): the color of the fruits on the tree.
				height (float): the height of the branches on the tree.
				location (tuple[int, int]): the location of the tree.
	
			Returns:
				bool: true if successful (the tree is not already logged).
			"""
			if not self.new_tree_discovered(location):
				return False
			self._trees[location[0]][location[1]] = Tree(color, height)
			self._fill_third_tree(location[0])
			return True
		
		def get_tree_color(self, location: tuple[int, int]) -> Signature | None:
			if self._at_location(location):
				return self._at_location(location).get_fruit_color()
				
		def get_tree_height(self, location: tuple[int, int]) -> float | None:
			if self._at_location(location):
				return self._at_location(location).get_height()
		
		def _fill_third_tree(self, row: int) -> None:
			"""
			If two of the three trees in a row are logged, the third can be calculated
	
			Params:
				row (int): The row of trees to check.
			"""
			if not self._at_location((row, 0)) and self._at_location((row, 1)) and self._at_location((row, 2)):
				fruit_color: Signature = self._at_location((row, 1)).get_fruit_color()
				fruit_height: float = 0
				for height in possible_heights:
					if not self._at_location((row, 1)).get_height() == height and not self._at_location((row, 2)).get_height() == height:
						fruit_height = height
				self._trees[row][0] = Tree(fruit_color, fruit_height)
			
			elif self._at_location((row, 0)) and not self._at_location((row, 1)) and self._at_location((row, 2)):
				fruit_color: Signature = self._at_location((row, 2)).get_fruit_color()
				fruit_height: float = 0
				for height in possible_heights:
					if not self._at_location((row, 2)).get_height() == height and not self._at_location((row, 0)).get_height() == height:
						fruit_height = height
				self._trees[row][1] = Tree(fruit_color, fruit_height)
			
			elif self._at_location((row, 0)) and self._at_location((row, 1)) and not self._at_location((row, 2)):
				fruit_color: Signature = self._at_location((row, 0)).get_fruit_color()
				fruit_height: float = 0
				for height in possible_heights:
					if not self._at_location((row, 0)).get_height() == height and not self._at_location((row, 1)).get_height() == height:
						fruit_height = height
				self._trees[row][2] = Tree(fruit_color, fruit_height)

	l = locals()
	l["FruitColor"] = FruitColor
	l["Tree"] = Tree
	l["Orchard"] = Orchard
	__ModuleCache__["src_tree"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_tree"]

def __define__src_movement():
	if "src_movement" in __ModuleCache__: return __ModuleCache__["src_movement"]
	__name__ = "__src_movement__"
	from vex import *
	
	class Log():
		"""
		Logs the changes in position of the robot, to find the current position relative to start.
		STATIC CLASS
	
		Params:
			_y_distance (float): forward is positive, and backward is negative.
			_x_distance (float): right is positive, and left is negative.
			_rot_angle (float): clockwise is positive, and counterclockwise is negative.
		"""
		_y_distance: float = 0 # forward positive, backward negative
		_x_distance: float = 0 # right positive, left negatvie
		_rot_angle: float = 0 # clockwise positive, counterclockwise negative
	
		@staticmethod
		def add_distance(y_distance: float = 0, x_distance: float = 0, rot_angle: float = 0) -> None:
			"""
			Adds respective values to the total.
	
			Params:
				y_distance (float): forward is positive, and backward is negative.
				x_distance (float): right is positive, and left is negative.
				rot_angle (float): clockwise is positive, and counterclockwise is negative.
			"""
			Log._y_distance += y_distance
			Log._x_distance += x_distance
			Log._rot_angle += rot_angle
		
		@staticmethod
		def get_y_distance() -> float:
			return Log._y_distance
		
		@staticmethod
		def get_x_distance() -> float:
			return Log._x_distance
		
		@staticmethod
		def get_rot_angle() -> float:
			return Log._rot_angle
		
		@staticmethod
		def return_to_origin():
			drive(0, -Log.get_x_distance(), -Log.get_rot_angle())
			drive(-Log.get_y_distance(), 0, 0)
	
	# motor names are based on top-down view with proper orientation
	northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
	northeast_motor: Motor = Motor(Ports.PORT8, 0.2, False) # set boolean so motor spins towards the front of the robot
	southwest_motor: Motor = Motor(Ports.PORT9, 0.2, True) # set boolean so motor spins towards the front of the robot
	southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot
	
	arm_motor_1 = Motor(Ports.PORT18, 0.2, True)
	arm_motor_2 = Motor(Ports.PORT14, 0.2, True)
	arm_motors = MotorGroup(arm_motor_1, arm_motor_2)
	claw_motor = Motor(Ports.PORT12, 0.2, True)
	door_motor = Motor(Ports.PORT1, 0.2, True)
	
	def drive(distance_y: float, distance_x: float, rotation_angle: float, speed: float = 40, stall: bool = True) -> None:
		"""
		Drives the robot.
	
		Params:
			distance_y (float): forward is positive, and backward is negative.
			distance_x (float): right is positive, and left is negative.
			rotation_angle (float): clockwise is positive, and counterclockwise is negative.
		"""
		wheel_diameter: float = 0
		degrees_y: float = distance_y / (wheel_diameter * math.pi) * 360
		degrees_x: float = distance_x / (wheel_diameter * math.pi) * 360
		degrees_r: float = distance_x / (wheel_diameter * math.pi) * 360 # need to solve
	
		northwest_motor.spin_for(FORWARD, degrees_y + degrees_x + degrees_r, DEGREES, speed, RPM, wait=False)
		northeast_motor.spin_for(FORWARD, degrees_y - degrees_x + degrees_r, DEGREES, speed, RPM, wait=False)
		southwest_motor.spin_for(FORWARD, degrees_y - degrees_x - degrees_r, DEGREES, speed, RPM, wait=False)
		southeast_motor.spin_for(FORWARD, degrees_y + degrees_x - degrees_r, DEGREES, speed, RPM, wait=stall)
		
		Log.add_distance(distance_y, distance_x, rotation_angle)
	
	def move_arm(end_position: float, speed: float = 75, stall: bool = True) -> None:
		"""
		Moves the arm.
	
		Params:
			end_position (float): the position of the arm after execution.
			speed (float): the speed the arm should traved (default is 75 RPM).
			stall (bool): wait for the arm to finish moving before moving on (default is true).
		"""
		arm_motors.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def move_claw(end_position: float, speed: int = 50, stall: bool = True) -> None:
		"""
		Moves the claw.
	
		Params:
			end_position (float): the position of the claw after execution.
			speed (float): the speed the claw should traved (default is 50 RPM).
			stall (bool): wait for the claw to finish moving before moving on (default is true).
		"""
		claw_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def squeeze() -> None:
		"""
		Squeezes the claw at a small speed, to better grip a fruit when pulling it down.
		"""
		claw_motor.spin(FORWARD, 5, RPM)
	
	# outwards: 1 = spin out, -1 = spin in
	def toggleDoor(angle: int = 360, outwards: int = 0, speed: float = 75) -> None:
		"""
		Moves the door, and automatically checks if complete.
	
		Params:
			angle (int): the angle to spin the door (default is 360 degrees).
			outwards (int): 1 = spin out, -1 = spin in, 0 = don't spin.
			speed (float): the speed to spin the door (default is 75 RPM).
		"""
		zero_position: vexnumber = 0
		door_motor.set_position(zero_position, DEGREES)
		door_motor.spin_for(FORWARD, outwards * angle, DEGREES, speed, RPM, wait=False)
		wait(200)
		if door_motor.is_spinning():
			door_motor.spin_to_position(0)
			toggleDoor(angle, outwards, speed)
	
	controller: Controller = Controller()
	y_button: Controller.Button = controller.buttonY
	right_button: Controller.Button = controller.buttonRight
	
	def kill() -> None:
		"""
		Checks if kill command on controller is executed.
		"""
		if y_button.pressing() and right_button.pressing():
			raise Exception("Kill Switch Triggered.")

	l = locals()
	l["Log"] = Log
	__ModuleCache__["src_movement"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_movement"]

def __define__src_routes():
	if "src_routes" in __ModuleCache__: return __ModuleCache__["src_routes"]
	__name__ = "__src_routes__"
	__root__src_movement = __define__src_movement()
	for k in __root__src_movement: locals()[k] = __root__src_movement[k]
	
	def go_to(location: tuple[int, int]):
		_go_to_row(location[0])
		_go_to_col(location[1])
	
	def _go_to_row(row: int):
		match row:
			case 0:
				drive(1, 0, 0)
			case 1:
				drive(1, 0, 0)
			case 2:
				drive(1, 0, 0)
	
	def _go_to_col(col: int):
		match col:
			case 0:
				drive(0, 1, 0)
			case 1:
				drive(0, 1, 0)
			case 2:
				drive(0, 1, 0)

	l = locals()
	__ModuleCache__["src_routes"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_routes"]

def __define__src_main():
	if "src_main" in __ModuleCache__: return __ModuleCache__["src_main"]
	__name__ = "__main__"
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
	__root__src_tree = __define__src_tree()
	FruitColor = __root__src_tree.FruitColor
	Orchard = __root__src_tree.Orchard
	__root__src_movement = __define__src_movement()
	for k in __root__src_movement: locals()[k] = __root__src_movement[k]
	__root__src_routes = __define__src_routes()
	for k in __root__src_routes: locals()[k] = __root__src_routes[k]
	
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
		go_to((0, 0))
		move_arm(5)
		move_claw(10)
		scan_fruit((0, 0))
		move_claw(0, stall=False)
		move_arm(0, stall=False)
		Log.return_to_origin()
	
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

	l = locals()
	__ModuleCache__["src_main"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_main"]

try: __define__src_main()
except Exception as e:
	s = [(25,"src\tree.py"),(165,"src\movement.py"),(310,"src\routes.py"),(342,"src\main.py"),(444,"<module>")]
	def f(x: str):
		if not x.startswith('  File'): return x
		l = int(match('.+line (\\d+),.+', x).group(1))
		for i in range(len(s)):
			if s[i][0] > l: return '  File {} line {} ({})'.format(s[i-1][1], l-s[i-1][0], l)
		return '  File {} line {} ({})'.format(s[-1][1], l-s[-1][0], l)
	buf = StringIO()
	print_exception(e, buf)
	print('\n'.join([f(x) for x in buf.getvalue().split("\n")]))
	exit(1)
