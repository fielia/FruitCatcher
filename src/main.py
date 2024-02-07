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
from control import move_drive, rotate_drive, rotate_arm, move_claw

# The controller
controller = Controller()
# Brain should be defined by default
brain = Brain()

# motor names are based on top-down view with proper orientation
northwest_motor: Motor = Motor(Ports.PORT1, 0.2, True) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT10, 0.2, False) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT1, 0.2, True) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT10, 0.2, False) # set boolean so motor spins towards the front of the robot
negative_motors: MotorGroup = MotorGroup(northwest_motor, southeast_motor) # the motors on the negative diagonal
positive_motors: MotorGroup = MotorGroup(northeast_motor, southwest_motor) # the motors on the positive diagonal

arm_motor = Motor(Ports.PORT11, 0.2, True) # take a look at params for validity
claw_motor = Motor(Ports.PORT12, 0.2, True)

button = Bumper(brain.three_wire_port.d)
range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM

def activate_control():
	while True:
		forward_speed, right_speed = move_drive(75)
		spin_speed: int = rotate_drive(75)
		northwest_motor.spin(FORWARD, forward_speed + right_speed + spin_speed, RPM)
		northeast_motor.spin(FORWARD, forward_speed - right_speed + spin_speed, RPM)
		southwest_motor.spin(FORWARD, forward_speed - right_speed - spin_speed, RPM)
		southeast_motor.spin(FORWARD, forward_speed + right_speed - spin_speed, RPM)

		arm_motor.spin(FORWARD, rotate_arm(), RPM)
		claw_motor.spin(FORWARD, move_claw(), RPM)

activate_control()
