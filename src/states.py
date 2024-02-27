from vex import *
from movement import Log, drive, rotate, move_arm, move_claw, toggle_squeeze, toggle_door, kill, reset_motors, reach_wall, go_to_bin_position, drop_fruit, reach_wall, controller, imu, brain, reach_bins, drive_speed
from routes import go_to_tree
from fruits import orchard, get_fruit, _center_on_fruit, _get_color
from tree import FruitColor

def test():
	test_row: int = 1
	# add testing code here
	print("starting test...")
	while True:
		_center_on_fruit(FruitColor.LEMON)
		brain.screen.clear_screen(Color.PURPLE)
		sleep(2000)
	print("uh oh")

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

current_tree: tuple[int, int] = (0, 0)

def travel_to_next_tree(trees_visited: int):
	global current_tree
	
	if trees_visited == 0:
		current_tree = (0, 0)
	elif trees_visited == 1:
		current_tree = (0, 1)
	elif trees_visited == 2:
		current_tree = (0, 2)
	elif trees_visited == 3:
		current_tree = (2, 0)
	elif trees_visited == 4:
		current_tree = (2, 1)
	elif trees_visited == 5:
		current_tree = (2, 2)
	elif trees_visited == 6:
		current_tree = (2, 0)
	elif trees_visited == 7:
		current_tree = (2, 1)
	elif trees_visited == 8:
		current_tree = (2, 2)

	go_to_tree(current_tree)

def obtain_fruit():
	get_fruit(current_tree)

def return_to_bins():
	rotate(90)
	reached: bool = False
	while not reached:
		reached = reach_wall()
	print("reached wall")
	reached = False
	while not reached:
		reached = reach_bins()
	print("reached bins")
	reached = False
	while not reached:
		reached = go_to_bin_position(FruitColor.LIME)# orchard.get_tree_color(current_tree))

def deposit_fruit():
	drop_fruit()

def reset_position():
	print("return to the start position")

### end of state functions

### start of transition functions

def end_idling() -> bool:
	if controller.buttonA.pressing():
		brain.screen.clear_screen()
		return True
	return False

### end of transition functions
