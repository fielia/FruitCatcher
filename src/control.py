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

door_open: bool = False # closed = false, open = true

def move_drive(speed: int = 100) -> tuple[int, int]:
	return (left_stick[0].position() * speed, left_stick[1].position() * speed)

def rotate_drive(speed: int = 100) -> int:
	return right_stick[0].position() * speed

def rotate_arm(speed: int = 100) -> int:
	if left_bumper.pressing():
		return speed
	elif right_bumper.pressing():
		return -speed
	else:
		return 0

def move_claw(speed: int = 100):
	if left_trigger.pressing():
		return speed
	elif right_trigger.pressing():
		return -speed
	else:
		return 0

# MAKE SURE THIS IS CALLED IN A SPIN_FOR
def toggleDoor(speed: int = 100):
	global door_open
	if a_button.pressing() and not door_open:
		door_open = True
		return speed
	elif b_button.pressing() and door_open:
		door_open = False
		return -speed
	else:
		return 0
