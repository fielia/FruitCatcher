from vex import Controller
controller: Controller = Controller()

left_stick: list[Controller.Axis] = [controller.axis1, controller.axis2]
right_stick: list[Controller.Axis] = [controller.axis3, controller.axis4]
left_bumper: Controller.Button = controller.buttonL1
right_bumper: Controller.Button = controller.buttonR1
left_trigger: Controller.Button = controller.buttonL2
right_trigger: Controller.Button = controller.buttonR2

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
