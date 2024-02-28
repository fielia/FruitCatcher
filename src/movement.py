from vex import *
from tree import FruitColor

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

	def add_distance(self, y_distance: float = 0, x_distance: float = 0, rot_angle: float = 0) -> None:
		"""
		Adds respective values to the total.

		Params:
			y_distance (float): forward is positive, and backward is negative.
			x_distance (float): right is positive, and left is negative.
			rot_angle (float): clockwise is positive, and counterclockwise is negative.
		"""
		self._y_distance += y_distance
		self._x_distance += x_distance
		self._rot_angle += rot_angle
	
	def get_y_distance(self) -> float:
		return self._y_distance
	
	def get_x_distance(self) -> float:
		return self._x_distance
	
	def get_rot_angle(self) -> float:
		return self._rot_angle

	def reset_log(self) -> None:
		self._y_distance = 0
		self._x_distance = 0
		self._rot_angle = 0
	
	def return_to_origin(self):
		drive(0, -self.get_x_distance())
		rotate(-self.get_rot_angle())
		drive(-self.get_y_distance(), 0)

# motor names are based on top-down view with proper orientation
brain = Brain()

northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT8, 0.2, True) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT9, 0.2, False) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot

arm_motor = Motor(Ports.PORT11, 0.2, True)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)

claw_motor.set_timeout(1500)

travel_log = Log()
distance_log = Log()

imu = Inertial(Ports.PORT20)

front_range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM
left_range_finder = Sonar(brain.three_wire_port.g)

def print_val():
	print(left_range_finder.distance(MM))

basket_sensor_1 = Light(brain.three_wire_port.b)
basket_sensor_2 = Light(brain.three_wire_port.a)

wheel_diameter: float = 100 # in mm
def drive(distance_y: float, distance_x: float, speed: float = 40, stall: bool = True, log: Log = distance_log) -> None:
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
	
	log.add_distance(y_distance=distance_y, x_distance=distance_x)

def drive_speed(speed_y: float = 40, speed_x: float = 40):
	northwest_motor.spin(FORWARD, speed_y + speed_x, RPM)
	northeast_motor.spin(FORWARD, speed_y - speed_x, RPM)
	southwest_motor.spin(FORWARD, speed_y - speed_x, RPM)
	southeast_motor.spin(FORWARD, speed_y + speed_x, RPM)

def rotate_speed(rotation_speed: float = 0):
	northwest_motor.spin(FORWARD, rotation_speed, RPM)
	northeast_motor.spin(FORWARD, -rotation_speed, RPM)
	southwest_motor.spin(FORWARD, rotation_speed, RPM)
	southeast_motor.spin(FORWARD, -rotation_speed, RPM)

def rotate(rotation_angle: float, speed: float = 40, stall: bool = True, log: Log = distance_log) -> None:
	"""
	Rotates the robot.

	Params:
		rotation_angle (float): the angle to rotate the robot.
		speed (float): the speed the wheel motors should spin (default is 40 RPM).
		stall (bool): wait for the motion to finish before moving on (default is true).
	"""
	robot_diameter: float = 380 # in mm
	if rotation_angle != 0:
		rotation_angle -= 10
	degrees_r: float = (robot_diameter * math.pi) * (rotation_angle / 360) / (wheel_diameter * math.pi) * 360
	print(degrees_r)
	
	northwest_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
	northeast_motor.spin_for(FORWARD, -degrees_r, DEGREES, speed, RPM, wait=False)
	southwest_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
	southeast_motor.spin_for(FORWARD, -degrees_r, DEGREES, speed, RPM, wait=stall)

	distance_log.add_distance(rot_angle=degrees_r)

def move_arm(end_position: float, speed: float = 100, stall: bool = True) -> None:
	"""
	Moves the arm.

	Params:
		end_position (float): the position of the arm after execution.
		speed (float): the speed the arm motor should spin (default is 75 RPM).
		stall (bool): wait for the arm to finish moving before moving on (default is true).
	"""
	kill()
	arm_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

def move_claw(end_position: float, speed: int = 70, stall: bool = True) -> None:
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

def reach_wall() -> bool:
	dist = left_range_finder.distance(DistanceUnits.CM)
	# print(dist)
	if abs(dist-15) > 2:
		error = dist*.75
		if error > 50:
			error = 50
		drive_speed(0, 20+error)
		return False
	else:
		drive_speed(0, 0)
		return True

past_side_dist: float = 0

def reach_bins() -> bool:
	# wall following to bin
	global past_side_dist

	dist: float = front_range_finder.distance(DistanceUnits.MM)

	if abs(dist-100) > 10: # if we are not at the bins yet
		# print("distance to go: "+str(dist-10))
		# orientation = imu.rotation()
		# print(orientation)
		# if abs(orientation) < 10: # if we are pointing relatively forwards...
			# adjust distance from the wall and keep going
		wall_dist = left_range_finder.distance(DistanceUnits.MM)
		if abs(wall_dist-past_side_dist) > 400: #ignore if it gets a crazy value
			wall_dist = past_side_dist
		else:
			past_side_dist = wall_dist
		effort = wall_dist - 180
		drive_speed(-20, effort / 10)
		return False
		# else:
			# heading_error = 0-orientation
			# heading_effort = 1*heading_error + 10
			# rotate_speed(heading_effort)
			# return False
	else:
		drive_speed(0, 0)
		print("FOLLOW_WALL -> POSITIONING_TO_BIN")
		return True

def go_to_bin_position(fruit_color: Signature) -> bool:
	# drive sideways to the correct bin

	# bins are 38cm wide
	# ultrasonic is 15cm away from the center of the bot
	bin_position: float = 0
	if fruit_color == FruitColor.LEMON:
		bin_position = 55
	elif fruit_color == FruitColor.LIME:
		bin_position = 450
	elif fruit_color == FruitColor.ORANGE_FRUIT:
		bin_position = 820

	wall_dist: float = left_range_finder.distance(DistanceUnits.MM)
	bin_dist: float = front_range_finder.distance(DistanceUnits.MM)
	# print("bin_dist: "+str(bin_dist))
	wall_error = wall_dist-bin_position
	bin_error = bin_dist-100
	if abs(bin_error) > 2000:
		return False
	if abs(wall_error) > 10 or abs(bin_error) > 10:
		y_effort = 0.1 * wall_error 	# move however far away from the wall
		x_effort = -0.05 * bin_error 				# stay 10cm in front of the bins
		drive_speed(x_effort, y_effort)
		return False
	else:
		drive_speed(0, 0)
		print("POSITIONING_TO_BIN -> DEPOSITING")
		return True
	


def _fruit_in_basket():
	# check both sides of the basket
	val_1 = basket_sensor_1.value()
	val_2 = basket_sensor_2.value()
	return val_1 < 2800 or val_2 < 2760

def drop_fruit():
	# print(val)
	ret_val = False
	if _fruit_in_basket(): # if there is still fruit in the basket
		# shake the fruit down the basket
		drive(40, 0,speed=100)
		drive(-40, 0, speed=100)
		toggle_door(180, 1)
		sleep(500)
		for i in range(2):
			drive(40, 0, speed=100)
			drive(-40, 0, speed=100)
		sleep(500)
		toggle_door(0)
		if _fruit_in_basket():
			drive(0, -10)
			toggle_door(180, -1)
			drive(0, 10)
		else:
			drive(0,0)
			print("DROP_FRUIT -> DONE!!")
			ret_val = True
	else:
		door_motor.spin_to_position(0, velocity=40)
		drive_speed(0, 0)
		print("DROP_FRUIT -> DONE!!")
		ret_val = True
	return ret_val

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
