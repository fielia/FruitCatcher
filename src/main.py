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
# from control import move_drive, rotate_drive, rotate_arm, move_claw
import random

# variable declaration
brain = Brain()

# motor names are based on top-down view with proper orientation
northwest_motor: Motor = Motor(Ports.PORT7, 0.2, False) # set boolean so motor spins towards the front of the robot
northeast_motor: Motor = Motor(Ports.PORT8, 0.2, False) # set boolean so motor spins towards the front of the robot
southwest_motor: Motor = Motor(Ports.PORT9, 0.2, True) # set boolean so motor spins towards the front of the robot
southeast_motor: Motor = Motor(Ports.PORT10, 0.2, True) # set boolean so motor spins towards the front of the robot
negative_motors: MotorGroup = MotorGroup(northwest_motor, southeast_motor) # the motors on the negative diagonal
positive_motors: MotorGroup = MotorGroup(northeast_motor, southwest_motor) # the motors on the positive diagonal

arm_motor = Motor(Ports.PORT18, 0.2, True)
claw_motor = Motor(Ports.PORT12, 0.2, True)
door_motor = Motor(Ports.PORT1, 0.2, True)
imu = Inertial(Ports.PORT20)
basket_sensor = Light(brain.three_wire_port.a)

button = Bumper(brain.three_wire_port.b)
front_range_finder = Sonar(brain.three_wire_port.e) # NOTE: has a range of 30 to 3000 MM
left_range_finder = Sonar(brain.three_wire_port.g)
fruit_range_finder = Sonar(brain.three_wire_port.c)

IDLE = 0
DRIVE_TO_WALL = 1
FOLLOW_WALL = 2
SCAN_FOR_BINS = 3
DONE = 4
bot_state = IDLE


controller: Controller = Controller()
# face buttons
y_button: Controller.Button = controller.buttonY
right_button: Controller.Button = controller.buttonRight

def drive_for(distance_x: float, distance_y: float, rotation_angle: float, speed: float = 40, stall: bool = True):
	wheel_diameter: float = 10
	degrees_x: float = distance_x / (wheel_diameter * math.pi) * 180
	degrees_y: float = distance_y / (wheel_diameter * math.pi) * 180
	degrees_r: float = rotation_angle # need to solve

	northwest_motor.spin_for(FORWARD, degrees_x + degrees_y + degrees_r, DEGREES, speed, RPM, wait=False)
	northeast_motor.spin_for(FORWARD, degrees_x - degrees_y + degrees_r, DEGREES, speed, RPM, wait=False)
	southwest_motor.spin_for(FORWARD, degrees_x - degrees_y - degrees_r, DEGREES, speed, RPM, wait=False)
	southeast_motor.spin_for(FORWARD, degrees_x + degrees_y - degrees_r, DEGREES, speed, RPM, wait=True)

def spin(forward: float, sideways: float, spin: float, speed: float = 40, stall: bool = True):
	# northwest_motor.spin()
	northwest_motor.spin(FORWARD, forward + sideways + spin, RPM)
	northeast_motor.spin(FORWARD, forward - sideways + spin, RPM)
	southwest_motor.spin(FORWARD, forward - sideways - spin, RPM)
	southeast_motor.spin(FORWARD, forward + sideways - spin, RPM)		

def move_arm(end_position: float, speed: float = 75, stall: bool = True):
	arm_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

def move_claw(end_position: float, speed: int = 50, stall: bool = True):
	claw_motor.spin_to_position(end_position, DEGREES, speed, RPM, wait=stall)

def squeeze():
	claw_motor.spin_for(FORWARD, 30, DEGREES, 5, RPM)

# outwards: 1 = spin out, -1 = spin in
def toggleDoor(angle: int = 360, outwards: int = 0, speed: float = 75, stall: bool = True):
	zero_position: vexnumber = 0
	door_motor.set_position(zero_position, DEGREES)
	door_motor.spin_for(FORWARD, outwards * angle, DEGREES, speed, RPM, wait=stall)
	wait(200)
	if door_motor.is_spinning():
		door_motor.spin_to_position(0)
		toggleDoor(angle, outwards, speed)

def start():
	global bot_state
	bot_state = DRIVE_TO_WALL
	print("IDLE -> DRIVE_TO_WALL")

def stop():
	northeast_motor.stop(HOLD)
	northwest_motor.stop(HOLD)
	southeast_motor.stop(HOLD)
	southwest_motor.stop(HOLD)

def drive_to_wall():
	global bot_state

	dist = left_range_finder.distance(DistanceUnits.CM)
	#print(dist)
	if dist>15:
		orientation = imu.rotation()
		spin_error = orientation*-0.2
		error = dist*.75
		if error > 50:
			error = 50
		spin(50+error, 0, spin_error)
	else:
		stop()
		bot_state = FOLLOW_WALL
		print("DRIVE_TO_WALL -> FOLLOW_WALL")

past_side_dist = 0
def follow_wall():
	global bot_state
	global past_side_dist

	dist = front_range_finder.distance(DistanceUnits.CM)

	if dist > 5: # if we are not at the bins yet
		orientation = imu.rotation()
		#print(orientation)
		if abs(orientation) < 10: # if we are pointing relatively forwards...
			# adjust distance from the wall and keep going
			spin_error = orientation*-.2
			side_dist = left_range_finder.distance(DistanceUnits.CM)
			if abs(side_dist-past_side_dist) > 40:
				side_dist = past_side_dist
			else:
				past_side_dist = side_dist
			effort = side_dist - 18
			spin(effort, -20, spin_error)
		else: # if we are orientated the wrong way...
			# spin to the correct orientation so that the sonar readings will be more accurate
			spin_error = orientation
			spin(0, 0, spin_error)

	else:
		bot_state = SCAN_FOR_BINS
		stop()
		print("FOLLOW_WALL -> SCAN_FOR_BINS")

def scan_for_bins():
	global bot_state

	val = basket_sensor.value()
	print(val)
	if val < 2800:
		door_motor.spin_for(FORWARD, 180, DEGREES, velocity=20)
		# door_motor.spin_for()
		drive_for(10, 0, 0, speed=100)
		drive_for(-10, 0, 0, speed=100)
	else:
		bot_state = DONE
		stop()
		print("SCAN_FOR_BINS -> DONE!!") 

button.pressed(start)
print("Calibrating...")
imu.calibrate()
print("Robot Armed")

while True:
	#if bot_state == IDLE:
		#print("IDLE")
	if bot_state == DRIVE_TO_WALL:
		drive_to_wall()
	elif bot_state == FOLLOW_WALL:
		follow_wall()
	elif bot_state == SCAN_FOR_BINS:
		scan_for_bins()
	elif bot_state == DONE:
		print("DONE!")
		sleep(500)