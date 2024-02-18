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
