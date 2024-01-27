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
right_light = Light(brain.three_wire_port.c) # light at value < 250, dark at value > 2500
front_button = Bumper(brain.three_wire_port.f)
left_light = Light(brain.three_wire_port.d) # light at value < 250, dark at value > 2500
back_button = Bumper(brain.three_wire_port.e)

default_speed = 100
boosted_speed = 125

left_motor.set_velocity(default_speed)
right_motor.set_velocity(default_speed)
drive_motors.set_velocity(default_speed, RPM)

def correct(direction: DirectionType.DirectionType, motor: Motor, light: Light, boost: bool): # boost: true = use boosted speed, false = use default speed
	modifier = 0
	if direction == FORWARD:
		modifier = 1
	elif direction == REVERSE:
		modifier = -1
	speed = 0
	if boost:
		speed =  boosted_speed
	else:
		speed = default_speed
	motor.set_velocity(modifier * speed)

def light_test():
	wait(500)
	brain.screen.clear_screen()
	left_correcting = False
	right_correcting = False
	while not front_button.pressing():
		drive_motors.spin(FORWARD)
		if not left_correcting and left_light.value() > 2500:
			correct(FORWARD, left_motor, left_light, True)
			left_correcting = True
		elif left_correcting and left_light.value() < 1000:
			correct(FORWARD, left_motor, left_light, False)
			left_correcting = False
		
		if not right_correcting and right_light.value() > 2500:
			correct(FORWARD, right_motor, right_light, True)
			right_correcting = True
		elif right_correcting and right_light.value() < 1000:
			correct(FORWARD, right_motor, right_light, False)
			right_correcting = False
	drive_motors.stop()
	brain.screen.print_at("Reverse Reverse!", x=50, y=100)
	wait(1000)
	brain.screen.clear_screen()
	while not back_button.pressing():
		drive_motors.spin(REVERSE)
		if not left_correcting and left_light.value() > 2500:
			correct(REVERSE, right_motor, left_light, True)
			left_correcting = True
		elif left_correcting and left_light.value() < 1000:
			correct(REVERSE, right_motor, left_light, False)
			left_correcting = False
		
		if not right_correcting and right_light.value() > 2500:
			correct(REVERSE, left_motor, right_light, True)
			right_correcting = True
		elif right_correcting and right_light.value() < 1000:
			correct(REVERSE, left_motor, right_light, False)
			right_correcting = False
	brain.screen.print_at("All Done.", x=50, y=100)
	drive_motors.stop()

'''while True:
	brain.screen.print_at(front_light.value(), x=50, y=50)
	wait(100) # used for discerning light sensor values
	brain.screen.clear_screen()'''

for i in range(5):
	brain.screen.print_at(left_light.value(), x=50, y=50)
	wait(100)
	brain.screen.print_at(right_light.value(), x=50, y=50)
	wait(100)
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)
front_button.pressed(light_test)
