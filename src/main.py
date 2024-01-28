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
import time

# The controller
controller = Controller()
# Brain should be defined by default
brain = Brain()

# TODO: confirm ports
left_motor = Motor(Ports.PORT11, 0.2, True)
right_motor = Motor(Ports.PORT15, 0.2, False)
drive_motors = MotorGroup(left_motor, right_motor)
arm_motor = Motor(Ports.PORT20, 0.2, True)
imu = Inertial(Ports.PORT13)

right_light = Light(brain.three_wire_port.d) # light at value < 250, dark at value > 2500
front_button = Bumper(brain.three_wire_port.f)
left_light = Light(brain.three_wire_port.c) # light at value < 250, dark at value > 2500
back_button = Bumper(brain.three_wire_port.e)

default_speed = 100
boosted_speed = 175

left_motor.set_velocity(default_speed)
right_motor.set_velocity(default_speed)
drive_motors.set_velocity(default_speed, RPM)

def correct(motor: Motor, light: Light, boost: bool): # boost: true = use boosted speed, false = use default speed
	speed = 0
	if boost:
		speed = boosted_speed
	else:
		speed = default_speed
	motor.set_velocity(speed)

def light_test():
	wait(1000)
	brain.screen.clear_screen()
	start_time = time.time()
	left_correcting = False
	right_correcting = False
	while not back_button.pressing():
		drive_motors.spin(REVERSE)
		if not left_correcting and left_light.value() > 2500:
			correct(left_motor, left_light, True)
			left_correcting = True
			brain.screen.print_at("Left: Correcting    ", x=50, y=50)
		elif left_correcting and left_light.value() < 1000:
			correct(left_motor, left_light, False)
			left_correcting = False
			brain.screen.print_at("Left: Not Correcting", x=50, y=50)
		
		if not right_correcting and right_light.value() > 2500:
			correct(right_motor, right_light, True)
			right_correcting = True	
			brain.screen.print_at("Right: Correcting    ", x=50, y=100)
		elif right_correcting and right_light.value() < 1000:
			correct(right_motor, right_light, False)
			right_correcting = False
			brain.screen.print_at("Right: Not Correcting", x=50, y=100)
	drive_motors.set_velocity(default_speed, RPM)
	drive_motors.spin_for(FORWARD, 180 * 5, DEGREES)
	imu.reset_heading()
	imu.set_heading(45)
	while imu.heading() <= 210:
		right_motor.spin(REVERSE)
		left_motor.spin(FORWARD)
	right_motor.stop()
	left_motor.stop()
	while not back_button.pressing():
		drive_motors.spin(REVERSE)
		if not left_correcting and left_light.value() > 2500:
			correct(left_motor, left_light, True)
			left_correcting = True
			brain.screen.print_at("Left: Correcting    ", x=50, y=50)
		elif left_correcting and left_light.value() < 1000:
			correct(left_motor, left_light, False)
			left_correcting = False
			brain.screen.print_at("Left: Not Correcting", x=50, y=50)
		
		if not right_correcting and right_light.value() > 2500:
			correct(right_motor, right_light, True)
			right_correcting = True	
			brain.screen.print_at("Right: Correcting    ", x=50, y=100)
		elif right_correcting and right_light.value() < 1000:
			correct(right_motor, right_light, False)
			right_correcting = False
			brain.screen.print_at("Right: Not Correcting", x=50, y=100)
	brain.screen.print_at("All Done.", x=50, y=150)
	drive_motors.stop()
	end_time = time.time()
	brain.screen.print_at(end_time - start_time, x=250, y=150)
	wait(5000)

'''while True:
	brain.screen.print_at(right_light.value(), x=50, y=50)
	wait(100) # used for discerning light sensor values
	brain.screen.clear_screen()'''

brain.screen.print_at(left_light.value(), x=50, y=50)
brain.screen.print_at(right_light.value(), x=50, y=50)
imu.calibrate()
while imu.is_calibrating():
	wait(100)
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)
front_button.pressed(light_test)
