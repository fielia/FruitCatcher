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

# TODO: confirm ports
left_motor = Motor(Ports.PORT11, 0.2, True)
right_motor = Motor(Ports.PORT15, 0.2, False)
drive_motors = MotorGroup(left_motor, right_motor)
arm_motor = Motor(Ports.PORT20, 0.2, True)
front_light = Light(brain.three_wire_port.c) # light at value < 250, dark at value > 2500
front_button = Bumper(brain.three_wire_port.f)
back_light = Light(brain.three_wire_port.d) # light at value < 250, dark at value > 2500
back_button = Bumper(brain.three_wire_port.e)

default_speed = 100
boosted_speed = 125

left_motor.set_velocity(default_speed)
right_motor.set_velocity(default_speed)
drive_motors.set_velocity(default_speed, RPM)

def light_test():
	wait(500)
	brain.screen.clear_screen()
	while not front_button.pressing():
		drive_motors.spin(FORWARD)
		right_motor.set_velocity(boosted_speed)
		brain.screen.print_at("Left! ", x=50, y=100)
		while front_light.value() < 2500 and not front_button.pressing():
			# keep spinning
			brain.screen.clear_line()
			brain.screen.print_at(front_light.value(), x=50, y=50)
		right_motor.set_velocity(default_speed)
		left_motor.set_velocity(boosted_speed)
		brain.screen.print_at("Right!", x=50, y=100)
		while front_light.value() > 1500 and not front_button.pressing():
			# keep spinning
			brain.screen.clear_line()
			brain.screen.print_at(front_light.value(), x=50, y=50)
		left_motor.set_velocity(default_speed)
	drive_motors.stop()
	brain.screen.print_at("Reverse Reverse!", x=50, y=100)
	wait(1000)
	brain.screen.clear_screen()
	while not back_button.pressing():
		drive_motors.spin(REVERSE)
		drive_motors.set_velocity(-default_speed, RPM)
		left_motor.set_velocity(-boosted_speed)
		brain.screen.print_at("Right!", x=50, y=100)
		while back_light.value() < 2500 and not back_button.pressing():
			# keep spinning
			brain.screen.clear_line()
			brain.screen.print_at(back_light.value(), x=50, y=50)
		left_motor.set_velocity(-default_speed)
		right_motor.set_velocity(-boosted_speed)
		brain.screen.print_at("Left! ", x=50, y=100)
		while back_light.value() > 1000 and not back_button.pressing():
			# keep spinning
			brain.screen.clear_line()
			brain.screen.print_at(back_light.value(), x=50, y=50)
		right_motor.set_velocity(-default_speed)
	brain.screen.print_at("All Done.", x=50, y=100)
	drive_motors.stop()

'''while True:
	brain.screen.print_at(front_light.value(), x=50, y=50)
	wait(100) # used for discerning light sensor values
	brain.screen.clear_screen()'''

for i in range(5):
	brain.screen.print_at(front_light.value(), x=50, y=50)
	wait(100)
	brain.screen.print_at(back_light.value(), x=50, y=50)
	wait(100)
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)
front_button.pressed(light_test)
