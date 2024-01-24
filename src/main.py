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

# The controller
controller = Controller()
# Brain should be defined by default
brain = Brain()

left_motor = Motor(Ports.PORT1, 0.2, True)
right_motor = Motor(Ports.PORT10, 0.2, False)
arm_motor = Motor(Ports.PORT8, 0.2, True) # take a look at params for validity
button = Bumper(brain.three_wire_port.d)
light_sensor = Light(brain.three_wire_port.e) # TODO: has a range of 30 to 3000 MM

drive_motors = MotorGroup(left_motor, right_motor)

arm_motor.set_velocity(150)

for i in range(10):
	brain.screen.print_at(light_sensor.
