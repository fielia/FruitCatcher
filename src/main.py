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
#from control import move_drive, rotate_drive, rotate_arm, move_claw

controller: Controller = Controller()

left_stick: list[Controller.Axis] = [controller.axis1, controller.axis2]
right_stick: list[Controller.Axis] = [controller.axis3, controller.axis4]
left_bumper: Controller.Button = controller.buttonL1
right_bumper: Controller.Button = controller.buttonR1
left_trigger: Controller.Button = controller.buttonL2
right_trigger: Controller.Button = controller.buttonR2

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


# The controller
controller = Controller()
# Brain should be defined by default
brain = Brain()

# motor names are based on top-down view with proper orientation
northwest_motor: Motor = Motor(Ports.PORT20, 0.2, False) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT19, 0.2, False) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT18, 0.2, True) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT17, 0.2, True) # set boolean so motor spins towards the front of the robot
negative_motors: MotorGroup = MotorGroup(northwest_motor, southeast_motor) # the motors on the negative diagonal
positive_motors: MotorGroup = MotorGroup(northeast_motor, southwest_motor) # the motors on the positive diagonal

arm_motor = Motor(Ports.PORT11, 0.2, True) # take a look at params for validity
claw_motor = Motor(Ports.PORT12, 0.2, True)

button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM

def activate_control():
	while True:
		forward_speed, right_speed = move_drive(5)
		spin_speed: int = rotate_drive(5)
		northwest_motor.spin(FORWARD, forward_speed + right_speed + spin_speed, RPM)
		northeast_motor.spin(FORWARD, forward_speed - right_speed + spin_speed, RPM)
		southwest_motor.spin(FORWARD, forward_speed - right_speed - spin_speed, RPM)
		southeast_motor.spin(FORWARD, forward_speed + right_speed - spin_speed, RPM)
#		arm_motor.spin(FORWARD, rotate_arm(), RPM)
#		claw_motor.spin(FORWARD, move_claw(), RPM)

activate_control()
