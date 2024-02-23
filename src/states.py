from vex import *
from movement import Log, drive, rotate, move_arm, move_claw, toggle_squeeze, toggle_door, kill, reset_motors, reach_wall, drop_fruit, reach_wall, controller, imu, brain
from routes import go_to_tree
from fruits import orchard, scan_fruit, CLAW_SQUEEZE, CLAW_CHOP, ARM_LOW, ARM_MID, ARM_HIGH

### state functions

# idling function
def pre_checks():
	imu.calibrate()
	brain.screen.print_at("IMU Calibrating...", x=50, y=50)
	while imu.is_calibrating():
		wait(100)
	reset_motors()
	brain.screen.clear_screen()
	brain.screen.print_at("Button Ready", x=50, y=50)

# temporary function that contains TRAVELING and GRABBING code
def activate_auto():
	"""
	What the robot executes.
	"""
	while controller.buttonA.pressing():
		wait(5)
	current_tree: tuple[int, int] = (0, 0)
	go_to_tree(current_tree)
	scan_fruit(current_tree)
	grab_fruit(orchard.get_tree_height(current_tree))
	Log.return_to_origin()

### end of state functions

def grab_fruit(fruit_height: float):
	move_arm(fruit_height)
	move_claw(CLAW_CHOP)
	move_claw(10, stall=False)
	move_arm(10, stall=True)
