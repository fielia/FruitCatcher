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
def __define__src_movement():
	if "src_movement" in __ModuleCache__: return __ModuleCache__["src_movement"]
	__name__ = "__src_movement__"
	
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
			drive(0, -Log.get_x_distance())
			rotate(-Log.get_rot_angle())
			drive(-Log.get_y_distance(), 0)
	
	# motor names are based on top-down view with proper orientation
	brain = Brain()
	
	northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
	northeast_motor: Motor = Motor(Ports.PORT8, 0.2, True) # set boolean so motor spins towards the front of the robot
	southwest_motor: Motor = Motor(Ports.PORT9, 0.2, False) # set boolean so motor spins towards the front of the robot
	southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot
	
	arm_motor = Motor(Ports.PORT11, 0.2, True)
	claw_motor = Motor(Ports.PORT12, 0.2, True)
	door_motor = Motor(Ports.PORT1, 0.2, True)
	
	imu = Inertial(Ports.PORT20)
	
	front_range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM
	left_range_finder = Sonar(brain.three_wire_port.g)
	
	basket_sensor_1 = Light(brain.three_wire_port.b)
	basket_sensor_2 = Light(brain.three_wire_port.a)
	
	wheel_diameter: float = 100 # in mm
	def drive(distance_y: float, distance_x: float, speed: float = 40, stall: bool = True) -> None:
		"""
		Drives the robot.
	
		Params (in MM):
			distance_y (float): forward is positive, and backward is negative.
			distance_x (float): right is positive, and left is negative.
			speed (float): the speed the wheel motors should spin (default is 40 RPM).
			stall (bool): wait for the motion to finish before moving on (default is true).
		"""
		kill()
		degrees_y: float = distance_y / (wheel_diameter * math.pi) * 360 / math.sqrt(2)
		degrees_x: float = distance_x / (wheel_diameter * math.pi) * 360 / math.sqrt(2)
		
		northwest_motor.spin_for(FORWARD, degrees_y + degrees_x, DEGREES, speed, RPM, wait=False)
		northeast_motor.spin_for(FORWARD, degrees_y - degrees_x, DEGREES, speed, RPM, wait=False)
		southwest_motor.spin_for(FORWARD, degrees_y - degrees_x, DEGREES, speed, RPM, wait=False)
		southeast_motor.spin_for(FORWARD, degrees_y + degrees_x, DEGREES, speed, RPM, wait=stall)
		
		Log.add_distance(y_distance=distance_y, x_distance=distance_x)
	
	def drive_speed(speed_y: float = 40, speed_x: float = 40):
		northwest_motor.spin(FORWARD, speed_y + speed_x, RPM)
		northeast_motor.spin(FORWARD, speed_y - speed_x, RPM)
		southwest_motor.spin(FORWARD, speed_y - speed_x, RPM)
		southeast_motor.spin(FORWARD, speed_y + speed_x, RPM)
	
	
	def rotate(rotation_angle: float, speed: float = 40, stall: bool = True) -> None:
		"""
		Rotates the robot.
	
		Params:
			rotation_angle (float): the angle to rotate the robot.
			speed (float): the speed the wheel motors should spin (default is 40 RPM).
			stall (bool): wait for the motion to finish before moving on (default is true).
		"""
		robot_diameter: float = 380 # in mm
		rotation_angle -= 10
		degrees_r: float = (robot_diameter * math.pi) * (rotation_angle / 360) / (wheel_diameter * math.pi) * 360
		print(degrees_r)
		
		northwest_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
		northeast_motor.spin_for(FORWARD, -degrees_r, DEGREES, speed, RPM, wait=False)
		southwest_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
		southeast_motor.spin_for(FORWARD, -degrees_r, DEGREES, speed, RPM, wait=stall)
	
		Log.add_distance(rot_angle=degrees_r)
	
	def move_arm(end_position: float, speed: float = 75, stall: bool = True) -> None:
		"""
		Moves the arm.
	
		Params:
			end_position (float): the position of the arm after execution.
			speed (float): the speed the arm motor should spin (default is 75 RPM).
			stall (bool): wait for the arm to finish moving before moving on (default is true).
		"""
		kill()
		arm_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def move_claw(end_position: float, speed: int = 50, stall: bool = True) -> None:
		"""
		Moves the claw.
	
		Params:
			end_position (float): the position of the claw after execution.
			speed (float): the speed the claw motor should spin (default is 50 RPM).
			stall (bool): wait for the claw to finish moving before moving on (default is true).
		"""
		kill()
		claw_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)
	
	def toggle_squeeze() -> None:
		"""
		Squeezes the claw at a small speed, to better grip a fruit when pulling it down.
		"""
		kill()
		if claw_motor.is_spinning():
			claw_motor.stop()
		else:
			claw_motor.spin(FORWARD, 5, RPM)
	
	# outwards: 1 = spin out, -1 = spin in
	def toggle_door(angle: int = 360, outwards: int = 1, speed: float = 75) -> None:
		"""
		Moves the door, and automatically checks if complete.
	
		Params:
			angle (int): the angle to spin the door (default is 360 degrees).
			outwards (int): 1 = spin out, -1 = spin in, 0 = don't spin.
			speed (float): the speed to spin the door (default is 75 RPM).
		"""
		kill()
		zero_position: vexnumber = 0
		door_motor.set_position(zero_position, DEGREES)
		door_motor.spin_for(FORWARD, outwards * angle, DEGREES, speed, RPM, wait=False)
		wait(1000)
		if door_motor.is_spinning():
			door_motor.spin_to_position(0)
			toggle_door(angle, outwards, speed)
	
	def reach_wall():
		dist = left_range_finder.distance(DistanceUnits.CM)
		# print(dist)
		if abs(dist-15) > 2:
			error = dist*.75
			if error > 50:
				error = 50
			drive_speed(20+error, 0)
		else:
			drive_speed(0, 0)
	
	past_side_dist = 0
	
	def go_to_bin_position(location: int):
		# wall following to bin, then reposition in front of correct bin
		nonlocal past_side_dist
	
		dist = front_range_finder.distance(DistanceUnits.CM)
	
	
		if abs(dist-10) > 1: # if we are not at the bins yet
			orientation = imu.rotation()
			#print(orientation)
			if abs(orientation) < 10: # if we are pointing relatively forwards...
				# adjust distance from the wall and keep going
				side_dist = left_range_finder.distance(DistanceUnits.CM)
				if abs(side_dist-past_side_dist) > 40:
					side_dist = past_side_dist
				else:
					past_side_dist = side_dist
				effort = side_dist - 18
				drive_speed(effort, -20)
			else: # if we are orientated the wrong way...
				# spin to the correct orientation so that the sonar readings will be more accurate
				spin_error = orientation
				spin_effort = spin_error * 1
				drive_speed(0, 0)
	
		else:
			drive_speed()
			print("FOLLOW_WALL -> SCAN_FOR_BINS")
	
	
	def _fruit_in_basket():
		# check both sides of the basket
		val_1 = basket_sensor_1.value()
		val_2 = basket_sensor_2.value()
		return val_1 < 2800 or val_2 < 2760
	
	def drop_fruit():
		# print(val)
		if _fruit_in_basket(): # if there is still fruit in the basket
			# shake the fruit down the basket
			drive(10, 0,speed=100)
			drive(-10, 0, speed=100)
			toggle_door(180, 1)
			sleep(500)
			for i in range(2):
				drive(10, 0, speed=100)
				drive(-10, 0, speed=100)
			sleep(500)
			toggle_door(0)
			if _fruit_in_basket():
				drive(0, -10)
				toggle_door(180, -1)
				drive(0, 10)
			else:
				drive(0,0)
				print("DROP_FRUIT -> DONE!!")
		else:
			door_motor.spin_to_position(0, velocity=40)
			drive_speed(0, 0)
			print("DROP_FRUIT -> DONE!!")
	
	controller: Controller = Controller()
	y_button: Controller.Button = controller.buttonY
	right_button: Controller.Button = controller.buttonRight
	
	def kill() -> None:
		"""
		Checks if kill command on controller is executed.
		"""
		if y_button.pressing() and right_button.pressing():
			raise Exception("Kill Switch Triggered.")
	
	def reset_motors() -> None:
		northwest_motor.set_position(0, DEGREES)
		northeast_motor.set_position(0, DEGREES)
		southwest_motor.set_position(0, DEGREES)
		southeast_motor.set_position(0, DEGREES)
		arm_motor.set_position(0, DEGREES)
		claw_motor.set_position(0, DEGREES)
		door_motor.set_position(0, DEGREES)

	l = locals()
	l["Log"] = Log
	l["brain"] = brain
	l["northwest_motor"] = northwest_motor
	l["northeast_motor"] = northeast_motor
	l["southwest_motor"] = southwest_motor
	l["southeast_motor"] = southeast_motor
	l["arm_motor"] = arm_motor
	l["claw_motor"] = claw_motor
	l["door_motor"] = door_motor
	l["imu"] = imu
	l["front_range_finder"] = front_range_finder
	l["left_range_finder"] = left_range_finder
	l["basket_sensor_1"] = basket_sensor_1
	l["basket_sensor_2"] = basket_sensor_2
	l["wheel_diameter"] = wheel_diameter
	l["drive"] = drive
	l["drive_speed"] = drive_speed
	l["rotate"] = rotate
	l["move_arm"] = move_arm
	l["move_claw"] = move_claw
	l["toggle_squeeze"] = toggle_squeeze
	l["toggle_door"] = toggle_door
	l["reach_wall"] = reach_wall
	l["past_side_dist"] = past_side_dist
	l["go_to_bin_position"] = go_to_bin_position
	l["_fruit_in_basket"] = _fruit_in_basket
	l["drop_fruit"] = drop_fruit
	l["controller"] = controller
	l["y_button"] = y_button
	l["right_button"] = right_button
	l["kill"] = kill
	l["reset_motors"] = reset_motors
	__ModuleCache__["src_movement"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_movement"]

def __define__src_routes():
	if "src_routes" in __ModuleCache__: return __ModuleCache__["src_routes"]
	__name__ = "__src_routes__"
	__root__src_movement = __define__src_movement()
	drive = __root__src_movement.drive
	
	at_door: bool = True # start corner of the robot (exit or opposite of exit)
	
	def go_to_tree(location: tuple[int, int]):
		_go_to_row_tree(location[0])
		_go_to_col_tree(location[1])
	
	def _go_to_row_tree(row: int):
		if at_door:
			if row == 0:
				drive(235, 0) # in mm
			elif row == 1:
				drive(1000, 0) # in mm
			elif row == 2:
				drive(1930, 0) # in mm
		else:
			if row == 0:
				drive(720, 0) # in mm
			elif row == 1:
				drive(1605, 0) # in mm
			elif row == 2:
				drive(2490, 0) # in mm
	
	def _go_to_col_tree(col: int):
		if at_door:
			if col == 0:
				drive(0, 440) # in mm
			elif col == 1:
				drive(0, 985) # in mm
			elif col == 2:
				drive(0, 1530) # in mm
		else:
			if col == 0:
				drive(0, 420) # in mm
			elif col == 1:
				drive(0, 955) # in mm
			elif col == 2:
				drive(0, 1510) # in mm

	l = locals()
	l["at_door"] = at_door
	l["go_to_tree"] = go_to_tree
	l["_go_to_row_tree"] = _go_to_row_tree
	l["_go_to_col_tree"] = _go_to_col_tree
	__ModuleCache__["src_routes"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_routes"]

def __define__src_tree():
	if "src_tree" in __ModuleCache__: return __ModuleCache__["src_tree"]
	__name__ = "__src_tree__"
	
	class FruitColor:
		"""
		An enum to better access the colors.
	
		Params:
				_sensitivity (float): the sensitivity value for each color.
		"""
	
		_sensitivity: float = 2
		GRAPEFRUIT: Signature = Signature(
			1, 6513, 7443, 6978, 1111, 1431, 1271, _sensitivity, 0
		)
		LIME: Signature = Signature(
			2, -6249, -5385, -5817, -3721, -3023, -3372, _sensitivity, 0
		)
		LEMON: Signature = Signature(
			3, 2607, 3087, 2846, -3461, -3199, -3330, _sensitivity, 0
		)
		ORANGE_FRUIT: Signature = Signature(
			4, 7581, 8071, 7826, -2049, -1809, -1929, _sensitivity, 0
		)
	
	possible_heights: list[float] = [17, 29, 38]
	class Tree:
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
	
		def __init__(self) -> None:
			self._height = 0
			self._num_picked = 0
	
		def get_fruit_color(self) -> Signature:
			return self._fruit_color
		
		def set_fruit_color(self, new_color: Signature) -> None:
			self._fruit_color = new_color
	
		def get_height(self) -> float:
			return self._height
		
		def set_height(self, new_height: float) -> None:
			self._height = new_height
	
		def picked_one(self) -> None:
			self._num_picked += 1
	
		def get_picked(self) -> int:
			return self._num_picked
		
		def exists(self) -> bool:
			return self._height != 0
	
	
	class Orchard:
		"""
		Represents the orchard, and contains all the trees.
	
		Params:
				_trees (List[List[Tree]]): a 2D array of the trees, with a higher-value index representing a tree farther away from origin.
		"""
	
		_trees: List[List[Tree]]
	
		def __init__(self) -> None:
			self._trees = [[Tree(), Tree(), Tree()], [Tree(), Tree(), Tree()], [Tree(), Tree(), Tree()]]
	
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
			return not self._at_location(location).exists()
	
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
			self._fill_colors(location[0], color)
			self._at_location(location).set_height(height)
			self._fill_third_tree(location[0])
			return True
	
		def get_tree_color(self, location: tuple[int, int]) -> Signature:
			if self._at_location(location):
				return self._at_location(location).get_fruit_color()
			raise Exception("Error: Tree at location " + str(location) + " not found. Query Variable: Color.")
	
		def get_tree_height(self, location: tuple[int, int]) -> float:
			if self._at_location(location).get_height() != 0:
				return self._at_location(location).get_height()
			raise Exception("Error: Tree at location " + str(location) + " not found. Query Variable: Height.")
	
		def _fill_colors(self, row: int, color: Signature) -> None:
			for tree in self._trees[row]:
				if not tree.exists():
					tree.set_fruit_color(color)
	
		def _fill_third_tree(self, row: int) -> None:
			"""
			If two of the three trees in a row are logged, the third can be calculated
	
			Params:
					row (int): The row of trees to check.
			"""
			if (
				not self._at_location((row, 0)).get_height() != 0
				and self._at_location((row, 1)).get_height() != 0
				and self._at_location((row, 2)).get_height() != 0
			):
				fruit_height: float = 0
				for height in possible_heights:
					if (
						not self._at_location((row, 1)).get_height() == height
						and not self._at_location((row, 2)).get_height() == height
					):
						fruit_height = height
				self._trees[row][0].set_height(fruit_height)
	
			elif (
				self._at_location((row, 0)).get_height() != 0
				and not self._at_location((row, 1)).get_height() != 0
				and self._at_location((row, 2)).get_height() != 0
			):
				fruit_height: float = 0
				for height in possible_heights:
					if (
						not self._at_location((row, 2)).get_height() == height
						and not self._at_location((row, 0)).get_height() == height
					):
						fruit_height = height
				self._trees[row][1].set_height(fruit_height)
	
			elif (
				self._at_location((row, 0)).get_height() != 0
				and self._at_location((row, 1)).get_height() != 0
				and not self._at_location((row, 2)).get_height() != 0
			):
				fruit_height: float = 0
				for height in possible_heights:
					if (
						not self._at_location((row, 0)).get_height() == height
						and not self._at_location((row, 1)).get_height() == height
					):
						fruit_height = height
				self._trees[row][2].set_height(fruit_height)

	l = locals()
	l["FruitColor"] = FruitColor
	l["possible_heights"] = possible_heights
	l["Tree"] = Tree
	l["Orchard"] = Orchard
	__ModuleCache__["src_tree"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_tree"]

def __define__src_fruits():
	if "src_fruits" in __ModuleCache__: return __ModuleCache__["src_fruits"]
	__name__ = "__src_fruits__"
	__root__src_tree = __define__src_tree()
	FruitColor = __root__src_tree.FruitColor
	Orchard = __root__src_tree.Orchard
	__root__src_movement = __define__src_movement()
	drive_speed = __root__src_movement.drive_speed
	move_arm = __root__src_movement.move_arm
	move_claw = __root__src_movement.move_claw
	brain = __root__src_movement.brain
	
	fruit_sonic = Sonar(brain.three_wire_port.c) # NOTE: has a range of 30 to 3000 MM
	camera = Vision(Ports.PORT14, 43, FruitColor.GRAPEFRUIT, FruitColor.LIME, FruitColor.LEMON, FruitColor.ORANGE_FRUIT)
	
	orchard = Orchard()
	
	CLAW_SQUEEZE: float = 90
	CLAW_CHOP: float = 115 # position of the claw right after chopping a fruit
	ARM_LOW: float = 125
	ARM_MID: float = 1040
	ARM_HIGH: float = 1925
	
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

	l = locals()
	l["fruit_sonic"] = fruit_sonic
	l["camera"] = camera
	l["orchard"] = orchard
	l["CLAW_SQUEEZE"] = CLAW_SQUEEZE
	l["CLAW_CHOP"] = CLAW_CHOP
	l["ARM_LOW"] = ARM_LOW
	l["ARM_MID"] = ARM_MID
	l["ARM_HIGH"] = ARM_HIGH
	l["_get_color"] = _get_color
	l["_get_height"] = _get_height
	l["scan_fruit"] = scan_fruit
	l["_convert_height"] = _convert_height
	l["center_on_fruit"] = center_on_fruit
	__ModuleCache__["src_fruits"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_fruits"]

def __define__src_states():
	if "src_states" in __ModuleCache__: return __ModuleCache__["src_states"]
	__name__ = "__src_states__"
	__root__src_movement = __define__src_movement()
	Log = __root__src_movement.Log
	drive = __root__src_movement.drive
	rotate = __root__src_movement.rotate
	move_arm = __root__src_movement.move_arm
	move_claw = __root__src_movement.move_claw
	toggle_squeeze = __root__src_movement.toggle_squeeze
	toggle_door = __root__src_movement.toggle_door
	kill = __root__src_movement.kill
	reset_motors = __root__src_movement.reset_motors
	reach_wall = __root__src_movement.reach_wall
	drop_fruit = __root__src_movement.drop_fruit
	reach_wall = __root__src_movement.reach_wall
	controller = __root__src_movement.controller
	imu = __root__src_movement.imu
	brain = __root__src_movement.brain
	__root__src_routes = __define__src_routes()
	go_to_tree = __root__src_routes.go_to_tree
	__root__src_fruits = __define__src_fruits()
	orchard = __root__src_fruits.orchard
	scan_fruit = __root__src_fruits.scan_fruit
	CLAW_SQUEEZE = __root__src_fruits.CLAW_SQUEEZE
	CLAW_CHOP = __root__src_fruits.CLAW_CHOP
	ARM_LOW = __root__src_fruits.ARM_LOW
	ARM_MID = __root__src_fruits.ARM_MID
	ARM_HIGH = __root__src_fruits.ARM_HIGH
	
	### state functions
	
	# idling function
	def pre_checks():
		imu.calibrate()
		brain.screen.print_at("IMU Calibrating...", x=50, y=50)
		while imu.is_calibrating():
			wait(100)
		reset_motors()
		brain.screen.clear_screen()
		brain.screen.print_at("Button Ready", x=50, y=50)
	
	# temporary function that contains TRAVELING and GRABBING code
	def activate_auto():
		"""
		What the robot executes.
		"""
		while controller.buttonA.pressing():
			wait(5)
		current_tree: tuple[int, int] = (0, 0)
		go_to_tree(current_tree)
		scan_fruit(current_tree)
		grab_fruit(orchard.get_tree_height(current_tree))
		Log.return_to_origin()
	
	### end of state functions
	
	def grab_fruit(fruit_height: float):
		move_arm(fruit_height)
		move_claw(CLAW_CHOP)
		move_claw(10, stall=False)
		move_arm(10, stall=True)

	l = locals()
	l["pre_checks"] = pre_checks
	l["activate_auto"] = activate_auto
	l["grab_fruit"] = grab_fruit
	__ModuleCache__["src_states"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_states"]

def __define__src_main():
	if "src_main" in __ModuleCache__: return __ModuleCache__["src_main"]
	__name__ = "__main__"
	# ---------------------------------------------------------------------------- #
	#                                                                              #
	# 	Module:       main.py                                                      #
	# 	Author:       ritvik                                                       #
	# 	Created:      2/14/2024, 8:33:31 AM                                       #
	# 	Description:  V5 project                                                   #
	#                                                                              #
	# ---------------------------------------------------------------------------- #
	
	# Library imports
	__root__src_states = __define__src_states()
	pre_checks = __root__src_states.pre_checks
	controller = __root__src_states.controller
	
	# state definitions
	IDLING = 0
	TRAVELING = 1
	SEARCHING = 2
	GRABBING = 3
	RETURNING = 4
	DEPOSITING = 5
	RESETTING = 6
	
	curr_state: int = IDLING
	
	def activate_auto():
		"""
		What the robot executes.
		"""
		nonlocal curr_state
		
		while True:
			if curr_state == IDLING:
				pre_checks()
				print("IDLING")
				while True:
					if controller.buttonA.pressing():
						curr_state = TRAVELING
						break
			elif curr_state == TRAVELING:
				print("TRAVELING")
			elif curr_state == SEARCHING:
				print("SEARCHING")
			elif curr_state == GRABBING:
				print("GRABBING")
			elif curr_state == RETURNING:
				print("RETURNING")
			elif curr_state == DEPOSITING:
				print("DEPOSITING")
			elif curr_state == RESETTING:
				print("RESETTING")
	
	
	# initialize testing (will be triggered with button press and pre-run checks will be run here)
	activate_auto()

	l = locals()
	l["IDLING"] = IDLING
	l["TRAVELING"] = TRAVELING
	l["SEARCHING"] = SEARCHING
	l["GRABBING"] = GRABBING
	l["RETURNING"] = RETURNING
	l["DEPOSITING"] = DEPOSITING
	l["RESETTING"] = RESETTING
	l["curr_state"] = curr_state
	l["activate_auto"] = activate_auto
	__ModuleCache__["src_main"] = __ModuleNamespace__(l)
	return __ModuleCache__["src_main"]

try: __define__src_main()
except Exception as e:
	s = [(20,"src\movement.py"),(323,"src\routes.py"),(375,"src\tree.py"),(561,"src\fruits.py"),(674,"src\states.py"),(744,"src\main.py"),(811,"<module>")]
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
