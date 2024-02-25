from vex import *
from movement import Log, drive, rotate, move_arm, move_claw, toggle_squeeze, toggle_door, kill, reset_motors, reach_wall, drop_fruit, reach_wall, controller, imu, brain
from routes import go_to_tree
from fruits import orchard, get_fruit

def test():
	# add testing code here
	get_fruit((0, 0))

### start of state functions

# idling function
def calibrate_sensors():
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
	get_fruit(current_tree)
	Log.return_to_origin()

### end of state functions

### start of transition functions

def end_idling() -> bool:
	if controller.buttonA.pressing():
		brain.screen.clear_screen()
		return True
	return False

### end of transition functions
