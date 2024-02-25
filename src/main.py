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

arm_motor = Motor(Ports.PORT11, 0.2, False)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)
imu = Inertial(Ports.PORT20)

button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM

# test function (runs teleoperation)
def activate_control():
	#while button.pressing():
	#	wait(5)
	# arm_motor.set_position(0)
	# claw_motor.set_position(0)
	while True:
		global door_opening

		forward_speed, right_speed = move_drive(1)
		spin_speed: float = rotate_drive(0.5)
		northwest_motor.spin(FORWARD, forward_speed + right_speed + spin_speed, RPM)
		northeast_motor.spin(FORWARD, forward_speed - right_speed + spin_speed, RPM)
		southwest_motor.spin(FORWARD, forward_speed - right_speed - spin_speed, RPM)
		southeast_motor.spin(FORWARD, forward_speed + right_speed - spin_speed, RPM)
		arm_motor.spin(FORWARD, move_arm(75), RPM)
		if controller.buttonLeft.pressing():
			print(arm_motor.position())
		door_motor.spin_for(FORWARD, toggleDoor(360), DEGREES, 75, RPM, False)
		if squeeze():
			claw_motor.spin(FORWARD, 5, RPM)
		else:
			claw_motor.spin(FORWARD, move_claw(30), RPM)
		if not door_motor.is_spinning():
			door_opening = False
		if button.pressing() or kill():
			break

# CODE FROM CONTROL.PY

controller: Controller = Controller()
# sticks
left_stick: list[Controller.Axis] = [controller.axis4, controller.axis3] # x, y
right_stick: list[Controller.Axis] = [controller.axis1, controller.axis2] # x, y
# top buttons
left_bumper: Controller.Button = controller.buttonL1
left_trigger: Controller.Button = controller.buttonL2
right_bumper: Controller.Button = controller.buttonR1
right_trigger: Controller.Button = controller.buttonR2
# face buttons
a_button: Controller.Button = controller.buttonA
b_button: Controller.Button = controller.buttonB
x_button: Controller.Button = controller.buttonX
y_button: Controller.Button = controller.buttonY
up_button: Controller.Button = controller.buttonUp
down_button: Controller.Button = controller.buttonDown
right_button: Controller.Button = controller.buttonRight
# function-specific fields
arm_displacement: int = 0 # arm displacement
MAX_ARM_DISPLACEMENT: int = 50 # maximum arm displacement before the arm comes off the track
ARM_DISPLACEMENT_ERROR: int = 5 # error in the limits for arm displacement
squeeze_state: bool = False # squeezing
door_opening: bool = False # closing = false, opening = true

def move_drive(speed: float = 100) -> tuple[float, float]:
	return (left_stick[0].position() * speed, left_stick[1].position() * speed)

def rotate_drive(speed: float = 100) -> float:
	return right_stick[0].position() * speed

def move_arm(speed: int = 100) -> int:
	if right_trigger.pressing():# and arm_displacement < MAX_ARM_DISPLACEMENT - ARM_DISPLACEMENT_ERROR:
		return speed
	elif right_bumper.pressing():# and arm_displacement > ARM_DISPLACEMENT_ERROR:
		return -speed
	else:
		return 0

def move_claw(speed: int = 50) -> int:
	if down_button.pressing():
		return speed
	elif up_button.pressing():
		return -speed
	else:
		return 0

def squeeze() -> bool:
	global squeeze_state
	if left_bumper.pressing() and not squeeze_state:
		squeeze_state = True
		return True
	elif left_trigger.pressing() and squeeze_state:
		squeeze_state = False
		return False
	else:
		return squeeze_state

# MAKE SURE THIS IS CALLED IN A SPIN_FOR
def toggleDoor(angle: int = 90) -> int:
	global door_opening
	if a_button.pressing() and not door_opening:
		door_opening = True
		zero_position: vexnumber = 0
		door_motor.set_position(zero_position, DEGREES)
		return angle
	elif x_button.pressing() and not door_opening:
		door_opening = True
		zero_position: vexnumber = 0
		door_motor.set_position(zero_position, DEGREES)
		return -angle
	elif b_button.pressing() and door_opening:
		door_motor.stop()
		door_motor.spin_to_position(0)
		return 0
	else:
		return 0

def kill() -> bool:
	return y_button.pressing() and right_button.pressing()

# initialize testing (will be triggered with button press and pre-run checks will be run here)
brain.screen.print("Teleop Activated")
activate_control()
