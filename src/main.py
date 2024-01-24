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

drive_motors.set_velocity(100)
arm_motor.set_velocity(150)

def light_test():
	drive_motors.spin(FORWARD)
	brain.screen.print_at("Forward!", x=50, y=100)
	while light_sensor.value() < 0: # TODO: confirm the value when at tape
		brain.screen.print_at(light_sensor.value(), x=50, y=50)
		wait(100)
	drive_motors.stop()
	wait(1000)
	drive_motors.spin(REVERSE)
	brain.screen.print_at("Reverse!", x=50, y=100)
	wait(250)
	while light_sensor.value() < 0: # TODO: confirm the value when at tape
		brain.screen.print_at(light_sensor.value(), x=50, y=50)
		wait(100)
	drive_motors.stop()
	wait(1000)

for i in range(10):
	brain.screen.print_at(light_sensor.value(), x=50, y=50)
	wait(100)
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)
button.pressed(light_test)
