from movement import *

def go_to(location: tuple[int, int]):
	_go_to_row(location[0])
	_go_to_col(location[1])

def _go_to_row(row: int):
	match row:
		case 0:
			drive(100, 0) # in mm
		case 1:
			drive(1000, 0) # in mm
		case 2:
			drive(1930, 0) # in mm

def _go_to_col(col: int):
	match col:
		case 0:
			drive(0, 430) # in mm
		case 1:
			drive(0, 985) # in mm
		case 2:
			drive(0, 1530) # in mm
