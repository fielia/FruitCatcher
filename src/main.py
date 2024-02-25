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
from states import calibrate_sensors, end_idling

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
	global curr_state
	
	while True:
		if curr_state == IDLING:
			calibrate_sensors()
			print("IDLING")
			while True:
				if end_idling():
					curr_state = TRAVELING
					break
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
activate_auto()
