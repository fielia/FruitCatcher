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
northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT8, 0.2, False) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT9, 0.2, True) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot

arm_motor_1 = Motor(Ports.PORT18, 0.2, True)
arm_motor_2 = Motor(Ports.PORT14, 0.2, True)
arm_motors = MotorGroup(arm_motor_1, arm_motor_2)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)

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

def rotate(rotation_angle: float, speed: float = 40, stall: bool = True) -> None:
	"""
	Rotates the robot.

	Params:
		rotation_angle (float): the angle to rotate the robot.
		speed (float): the speed the wheel motors should spin (default is 40 RPM).
		stall (bool): wait for the motion to finish before moving on (default is true).
	"""
	degrees_r: float = rotation_angle / (wheel_diameter * math.pi) * 360 # need to solve
	
	northwest_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
	northeast_motor.spin_for(FORWARD, degrees_r, DEGREES, speed, RPM, wait=False)
	southwest_motor.spin_for(FORWARD, -degrees_r, DEGREES, speed, RPM, wait=False)
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
	arm_motors.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

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
	kill()
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
