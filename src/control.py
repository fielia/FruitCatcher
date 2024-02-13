# this code is identical to the code at the bottom of main.py
# if changes are needed, this file must also be updated (recommended that this file changes first, then copied to main.py)

from vex import Controller
controller: Controller = Controller()
# sticks
left_stick: list[Controller.Axis] = [controller.axis4, controller.axis3] # x, y
right_stick: list[Controller.Axis] = [controller.axis1, controller.axis2] # x, y
# top buttons
left_bumper: Controller.Button = controller.buttonL1
right_bumper: Controller.Button = controller.buttonR1
left_trigger: Controller.Button = controller.buttonL2
right_trigger: Controller.Button = controller.buttonR2
# face buttons
a_button: Controller.Button = controller.buttonA
b_button: Controller.Button = controller.buttonB
y_button: Controller.Button = controller.buttonY
down_button: Controller.Button = controller.buttonDown
# function-specific fields
arm_displacement: int = 0 # arm displacement
MAX_ARM_DISPLACEMENT: int = 50 # maximum arm displacement before the arm comes off the track
ARM_DISPLACEMENT_ERROR: int = 5 # error in the limits for arm displacement
door_open: bool = False # closed = false, open = true

def move_drive(speed: int = 100) -> tuple[int, int]:
	return (left_stick[0].position() * speed, left_stick[1].position() * speed)

def rotate_drive(speed: int = 100) -> int:
	return right_stick[0].position() * speed

def move_arm(speed: int = 100) -> int:
	if left_bumper.pressing() and arm_displacement < MAX_ARM_DISPLACEMENT - ARM_DISPLACEMENT_ERROR:
		return speed
	elif right_bumper.pressing() and arm_displacement > ARM_DISPLACEMENT_ERROR:
		return -speed
	else:
		return 0

def move_claw(speed: int = 100) -> int:
	if left_trigger.pressing():
		return speed
	elif right_trigger.pressing():
		return -speed
	else:
		return 0

# MAKE SURE THIS IS CALLED IN A SPIN_FOR
def toggleDoor(speed: int = 100) -> int:
	global door_open
	if a_button.pressing() and not door_open:
		door_open = True
		return speed
	elif b_button.pressing() and door_open:
		door_open = False
		return -speed
	else:
		return 0

def kill() -> bool:
	return y_button.pressing() and down_button.pressing()
