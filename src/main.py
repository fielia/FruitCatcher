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
# from control import move_drive, rotate_drive, rotate_arm, move_claw

# variable declaration
brain = Brain()

# motor names are based on top-down view with proper orientation
northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT8, 0.2, False) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT9, 0.2, True) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot
negative_motors: MotorGroup = MotorGroup(northwest_motor, southeast_motor) # the motors on the negative diagonal
positive_motors: MotorGroup = MotorGroup(northeast_motor, southwest_motor) # the motors on the positive diagonal

arm_motor_1 = Motor(Ports.PORT18, 0.2, True)
arm_motor_2 = Motor(Ports.PORT14, 0.2, True)
arm_motors = MotorGroup(arm_motor_1, arm_motor_2)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)
imu = Inertial(Ports.PORT20)

button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM

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

# CODE FROM CONTROL.PY

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
		

def move_arm(end_position: float, speed: float = 75, stall: bool = True):
	arm_motors.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

def move_claw(end_position: float, speed: int = 50, stall: bool = True):
	claw_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

def squeeze():
	claw_motor.spin(FORWARD, 5, RPM)

# outwards: 1 = spin out, -1 = spin in
def toggleDoor(angle: int = 360, outwards: int = 0, speed: float = 75, stall: bool = True):
	zero_position: vexnumber = 0
	door_motor.set_position(zero_position, DEGREES)
	door_motor.spin_for(FORWARD, outwards * angle, DEGREES, speed, RPM, wait=stall)
	wait(200)
	if door_motor.is_spinning():
		door_motor.spin_to_position(0)
		toggleDoor(angle, outwards, speed)

def kill() -> bool:
	return y_button.pressing() and right_button.pressing()

# initialize testing (will be triggered with button press and pre-run checks will be run here)
brain.screen.print("Teleop Activated")
activate_control()
