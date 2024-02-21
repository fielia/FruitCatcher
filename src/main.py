# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ritvik                                                       #
# 	Created:      2/14/2024, 8:33:31 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from states import brain, imu, reset_motors, controller

# state definitions
IDLING = 0
TRAVELING = 1
SEARCHING = 2
GRABBING = 3
RETURNING = 4
DEPOSITING = 5
RESETTING = 6

curr_state: int = IDLING

def activate_auto():
	"""
	What the robot executes.
	"""
	while True:
		if curr_state == IDLING:
			print("IDLING")
		elif curr_state == TRAVELING:
			print("TRAVELING")
		elif curr_state == SEARCHING:
			print("SEARCHING")
		elif curr_state == GRABBING:
			print("GRABBING")
		elif curr_state == RETURNING:
			print("RETURNING")
		elif curr_state == DEPOSITING:
			print("DEPOSITING")
		elif curr_state == RESETTING:
			print("RESETTING")


# initialize testing (will be triggered with button press and pre-run checks will be run here)
imu.calibrate()
brain.screen.print_at("IMU Calibrating...", x=50, y=50)
while imu.is_calibrating():
	wait(100)
reset_motors()
brain.screen.clear_screen()
brain.screen.print_at("Button Ready", x=50, y=50)

controller.buttonA.pressed(activate_auto)
