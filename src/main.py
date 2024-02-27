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
from states import test, calibrate_sensors, end_idling, travel_to_next_tree, obtain_fruit, return_to_bins, deposit_fruit, reset_position

# state definitions
IDLING = 0
TRAVELING = 1
OBTAINING = 2
RETURNING = 3
DEPOSITING = 4
RESETTING = 5

curr_state: int = IDLING # don't run normal code

testing: bool = False

def activate_auto():
	"""
	What the robot executes.
	"""
	global curr_state

	print('activate auto')

	if testing:
		test()
		print("OBTAINING")
		# wait(10000) # now put the fruit
		# obtain_fruit()
		print("obtained")

	trees_visited: int = 0
	
	while True:
		if curr_state == IDLING:
			print("IDLING")
			calibrate_sensors()
			while True:
				if end_idling():
					curr_state = TRAVELING
					break
		elif curr_state == TRAVELING:
			print("TRAVELING")
			travel_to_next_tree(trees_visited)
			trees_visited += 1
			curr_state = OBTAINING
		elif curr_state == OBTAINING:
			print("OBTAINING")
			# wait(10000) # now put the fruit
			obtain_fruit()
			if trees_visited % 3 == 0:
				curr_state = RETURNING
			else:
				curr_state = TRAVELING
		elif curr_state == RETURNING:
			print("RETURNING")
			return_to_bins()
			curr_state = DEPOSITING
		elif curr_state == DEPOSITING:
			print("DEPOSITING")
			deposit_fruit()
			curr_state = RESETTING
		elif curr_state == RESETTING:
			print("RESETTING")
			reset_position()
			curr_state = TRAVELING
			return


# initialize testing (will be triggered with button press and pre-run checks will be run here)
activate_auto()
