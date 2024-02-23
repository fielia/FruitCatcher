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
	global past_side_dist

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
