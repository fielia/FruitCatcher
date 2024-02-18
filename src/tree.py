from vex import *
class FruitColor():
	sensitivity: float = 2
	GRAPEFRUIT = Signature(1, 6513, 7443, 6978, 1111, 1431, 1271, sensitivity, 0)
	LIME = Signature(2, -6249, -5385, -5817, -3721, -3023, -3372, sensitivity, 0)
	LEMON = Signature(3, 2607, 3087, 2846, -3461, -3199, -3330, sensitivity, 0)
	ORANGE_FRUIT = Signature(4, 7581, 8071, 7826, -2049, -1809, -1929, sensitivity, 0)		

possible_heights: list[float] = [17, 29, 38] # just for reference
class Tree():
	_fruit_color: Signature
	_height: float
	_num_picked: int # range is 0-4 for how many have been picked

	def __init__(self, fruit_color: Signature, height: float) -> None:
		self._fruit_color = fruit_color
		self._height = height
		self._num_picked = 0
	
	def get_fruit_color(self) -> Signature:
		return self._fruit_color
	
	def get_height(self) -> float:
		return self._height
	
	def picked_one(self) -> None:
		self._num_picked += 1

	def get_picked(self) -> int:
		return self._num_picked

class Orchard():
	_trees: List[List[Tree]]

	def __init__(self) -> None:
		self._trees = [[], [], []]

	def _at_location(self, location: tuple[int, int]):
		return self._trees[location[0]][location[1]]
	
	def new_tree_discovered(self, location: tuple[int, int]) -> bool:
		return not self._at_location(location)

	def add_tree(self, color: Signature, height: float, location: tuple[int, int]) -> bool: # true if success, false if already present
		if not self.new_tree_discovered(location):
			return False
		self._trees[location[0]][location[1]] = Tree(color, height)
		self._fill_third_tree(location[0])
		return True
	
	def get_tree_color(self, location: tuple[int, int]) -> Signature | None:
		if self._at_location(location):
			return self._at_location(location).get_fruit_color()
			
	def get_tree_height(self, location: tuple[int, int]) -> float | None:
		if self._at_location(location):
			return self._at_location(location).get_height()
	
	def _fill_third_tree(self, row: int) -> None:
		if not self._at_location((row, 0)) and self._at_location((row, 1)) and self._at_location((row, 2)):
			fruit_color: Signature = self._at_location((row, 1)).get_fruit_color()
			fruit_height: float = 0
			for height in possible_heights:
				if not self._at_location((row, 1)).get_height() == height and not self._at_location((row, 2)).get_height() == height:
					fruit_height = height
			self._trees[row][0] = Tree(fruit_color, fruit_height)
		
		elif self._at_location((row, 0)) and not self._at_location((row, 1)) and self._at_location((row, 2)):
			fruit_color: Signature = self._at_location((row, 2)).get_fruit_color()
			fruit_height: float = 0
			for height in possible_heights:
				if not self._at_location((row, 2)).get_height() == height and not self._at_location((row, 0)).get_height() == height:
					fruit_height = height
			self._trees[row][1] = Tree(fruit_color, fruit_height)
		
		elif self._at_location((row, 0)) and self._at_location((row, 1)) and not self._at_location((row, 2)):
			fruit_color: Signature = self._at_location((row, 0)).get_fruit_color()
			fruit_height: float = 0
			for height in possible_heights:
				if not self._at_location((row, 0)).get_height() == height and not self._at_location((row, 1)).get_height() == height:
					fruit_height = height
			self._trees[row][2] = Tree(fruit_color, fruit_height)
