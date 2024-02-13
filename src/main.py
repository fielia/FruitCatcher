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

arm_motor = Motor(Ports.PORT18, 0.2, True)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)
imu = Inertial(Ports.PORT20)

button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM

# test function (runs teleoperation)
def activate_control():
	while True:
		forward_speed, right_speed = move_drive(25)
		spin_speed: int = rotate_drive(25)
		northwest_motor.spin(FORWARD, forward_speed + right_speed + spin_speed, RPM)
		northeast_motor.spin(FORWARD, forward_speed - right_speed + spin_speed, RPM)
		southwest_motor.spin(FORWARD, forward_speed - right_speed - spin_speed, RPM)
		southeast_motor.spin(FORWARD, forward_speed + right_speed - spin_speed, RPM)
		arm_motor.spin(FORWARD, rotate_arm(), RPM)
		claw_motor.spin(FORWARD, move_claw(), RPM)
		door_motor.spin_for(FORWARD, 75 * 5, DEGREES, toggleDoor(), RPM, False)

# CODE FROM CONTROL.PY

controller: Controller = Controller()
# sticks
left_stick: list[Controller.Axis] = [controller.axis4, controller.axis3] # x, y
right_stick: list[Controller.Axis] = [controller.axis1, controller.axis2] # x, y
# top buttons
left_bumper: Controller.Button = controller.buttonL1
right_bumper: Controller.Button = controller.buttonR1
left_trigger: Controller.Button = controller.buttonL2
right_trigger: Controller.Button = controller.buttonR2
# face buttons
a_button: Controller.Button = controller.buttonA
b_button: Controller.Button = controller.buttonB

door_open: bool = False # closed = false, open = true

def move_drive(speed: int = 100) -> tuple[int, int]:
	return (left_stick[0].position() * speed, left_stick[1].position() * speed)

def rotate_drive(speed: int = 100) -> int:
	return right_stick[0].position() * speed

def rotate_arm(speed: int = 100) -> int:
	if left_bumper.pressing():
		return speed
	elif right_bumper.pressing():
		return -speed
	else:
		return 0

def move_claw(speed: int = 100):
	if left_trigger.pressing():
		return speed
	elif right_trigger.pressing():
		return -speed
	else:
		return 0

# MAKE SURE THIS IS CALLED IN A SPIN_FOR
def toggleDoor(speed: int = 100):
	global door_open
	if a_button.pressing() and not door_open:
		door_open = True
		return speed
	elif b_button.pressing() and door_open:
		door_open = False
		return -speed
	else:
		return 0

# initialize testing (will be triggered with button press and pre-run checks will be run here)
brain.screen.print("Teleop Activated")
activate_control()
