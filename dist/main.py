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
		sensitivity: float = 2
		GRAPEFRUIT = Signature(1, 6513, 7443, 6978, 1111, 1431, 1271, sensitivity, 0)
		LIME = Signature(2, -6249, -5385, -5817, -3721, -3023, -3372, sensitivity, 0)
		LEMON = Signature(3, 2607, 3087, 2846, -3461, -3199, -3330, sensitivity, 0)
		ORANGE_FRUIT = Signature(4, 7581, 8071, 7826, -2049, -1809, -1929, sensitivity, 0)		
	
	possible_heights: list[float] = [17, 29, 38] # just for reference
	class Tree():
		_fruit_color: Signature
		_height: float
		_num_picked: int # range is 0-4 for how many have been picked
	
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
		_trees: List[List[Tree]]
	
		def __init__(self) -> None:
			self._trees = [[], [], []]
	
		def _at_location(self, location: tuple[int, int]):
			return self._trees[location[0]][location[1]]
		
		def new_tree_discovered(self, location: tuple[int, int]) -> bool:
			return not self._at_location(location)
	
		def add_tree(self, color: Signature, height: float, location: tuple[int, int]) -> bool: # true if success, false if already present
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
		_y_distance: float # forward positive, backward negative
		_x_distance: float # right positive, left negatvie
		_rot_angle: float # clockwise positive, counterclockwise negative
	
		def __init__(self) -> None:
			self._y_distance = 0
			self._x_distance = 0
			self._rot_angle = 0
	
		def add_distance(self, y_distance: float = 0, x_distance: float = 0, rot_angle: float = 0):
			self._y_distance += y_distance
			self._x_distance += x_distance
			self._rot_angle += rot_angle
		
		def get_y_distance(self) -> float:
			return self._y_distance
		
		def get_x_distance(self) -> float:
			return self._x_distance
		
		def get_rot_angle(self) -> float:
			return self._rot_angle
	
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
	
	
	controller: Controller = Controller()
	# face buttons
	y_button: Controller.Button = controller.buttonY
	right_button: Controller.Button = controller.buttonRight
	
	def drive(distance_x: float, distance_y: float, rotation_angle: float, speed: float = 40, stall: bool = True):
		wheel_diameter: float = 0
		degrees_x: float = distance_x / (wheel_diameter * math.pi) * 360
		degrees_y: float = distance_y / (wheel_diameter * math.pi) * 360
		degrees_r: float = distance_x / (wheel_diameter * math.pi) * 360 # need to solve
	
		northwest_motor.spin_for(FORWARD, degrees_x + degrees_y + degrees_r, DEGREES, speed, RPM, wait=False)
		northeast_motor.spin_for(FORWARD, degrees_x - degrees_y + degrees_r, DEGREES, speed, RPM, wait=False)
		southwest_motor.spin_for(FORWARD, degrees_x - degrees_y - degrees_r, DEGREES, speed, RPM, wait=False)
		southeast_motor.spin_for(FORWARD, degrees_x + degrees_y - degrees_r, DEGREES, speed, RPM, wait=stall)
	
	def move_arm(end_position: float, speed: float = 75, stall: bool = True) -> None:
		arm_motors.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def move_claw(end_position: float, speed: int = 50, stall: bool = True) -> None:
		claw_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def squeeze() -> None:
		claw_motor.spin(FORWARD, 5, RPM)
	
	# outwards: 1 = spin out, -1 = spin in
	def toggleDoor(angle: int = 360, outwards: int = 0, speed: float = 75, stall: bool = True) -> None:
		zero_position: vexnumber = 0
		door_motor.set_position(zero_position, DEGREES)
		door_motor.spin_for(FORWARD, outwards * angle, DEGREES, speed, RPM, wait=stall)
		wait(200)
		if door_motor.is_spinning():
			door_motor.spin_to_position(0)
			toggleDoor(angle, outwards, speed)
	
	def kill() -> None:
		if y_button.pressing() and right_button.pressing():
			raise Exception("Kill Switch Triggered.")

	l = locals()
	l["Log"] = Log
	__ModuleCache__["src_movement"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_movement"]

def __define__src_routes():
	if "src_routes" in __ModuleCache__: return __ModuleCache__["src_routes"]
	__name__ = "__src_routes__"

	l = locals()
	__ModuleCache__["src_routes"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_routes"]

def __define__src_main():
	if "src_main" in __ModuleCache__: return __ModuleCache__["src_main"]
	__name__ = "__main__"
	# ---------------------------------------------------------------------------- #
	#                                                                              #
	# 	Module:       main.py                                                      #
	# 	Author:       ritvi                                                        #
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
	
	# test function (runs teleoperation)
	def activate_control():
		while button.pressing():
			wait(5)
		drive(100, 0, 0)
		move_arm(5)
		move_claw(10)
		move_claw(0, stall=False)
		move_arm(0, stall=False)
		drive(-100, 0, 0)
		scan_fruit((0, 0))
	
	# CODE FROM CONTROL.PY
	
	def get_color() -> Signature:
		COLORS = [FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT]
		for color in COLORS:
			objects: Tuple[VisionObject] = camera.take_snapshot(color, 1)
			if objects:
				return color
	
		brain.screen.print_at("No fruit found.   ", x=50, y=100)
		raise Exception("Camera did not detect a fruit.")
	
	def get_height() -> float:
		
		height = fruit_sonic.distance(DistanceUnits.CM)
		if height > 20:
			raise Exception("Ultrasonic did not detect a fruit.")
		return height
	
	def scan_fruit(location: tuple[int, int]) -> None:
		fruit_color: Signature = get_color()
		height: float = get_height()
		orchard.add_tree(fruit_color, convert_height(height), location)
	
	def convert_height(old_height: float) -> float: # takes a raw value from the ultrasonic and returns the height of the fruit above the ground
		return old_height
	
	# initialize testing (will be triggered with button press and pre-run checks will be run here)
	brain.screen.print("Teleop Activated")
	activate_control()

	l = locals()
	__ModuleCache__["src_main"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_main"]

try: __define__src_main()
except Exception as e:
	s = [(25,"src\tree.py"),(118,"src\movement.py"),(204,"src\routes.py"),(212,"src\main.py"),(289,"<module>")]
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
