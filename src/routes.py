from movement import travel_log, drive

# TODO: CHANGE ROUTES TO START AT BINS
def go_to_tree(location: tuple[int, int]):
	if location[1] == 0:
		_go_to_row_tree(location[0])
	else:
		travel_log.return_to_origin()
	_go_to_col_tree(location[1])
	

def _go_to_row_tree(row: int):
	if row == 0:
		drive(0, 400, log=travel_log) # in mm
	elif row == 1:
		drive(0, 1400, log=travel_log)
	elif row == 2:
		drive(0, 2330, log=travel_log)

def _go_to_col_tree(col: int):
	if col == 0:
		drive(600, 0, log=travel_log)
		drive(0, 20, log=travel_log)
	elif col == 1:
		drive(0, -200, log=travel_log)
		drive(650, 0, log=travel_log)
		drive(0, 175, log=travel_log)
	elif col == 2:
		drive(0, -200, log=travel_log)
		drive(600, 0, log=travel_log)
		drive(0, 175, log=travel_log)
	travel_log.reset_log()
