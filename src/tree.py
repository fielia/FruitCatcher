from vex import *

class FruitColor():
	"""
	An enum to better access the colors.

	Params:
		_sensitivity (float): the sensitivity value for each color.
	"""
	_sensitivity: float = 2
	GRAPEFRUIT: Signature = Signature(1, 6513, 7443, 6978, 1111, 1431, 1271, _sensitivity, 0)
	LIME: Signature = Signature(2, -6249, -5385, -5817, -3721, -3023, -3372, _sensitivity, 0)
	LEMON: Signature = Signature(3, 2607, 3087, 2846, -3461, -3199, -3330, _sensitivity, 0)
	ORANGE_FRUIT: Signature = Signature(4, 7581, 8071, 7826, -2049, -1809, -1929, _sensitivity, 0)

possible_heights: list[float] = [17, 29, 38]
class Tree():
	"""
	Represents one tree on the field.
 
	Params:
		_fruit_color (Signature): the color of the fruits on the tree.
		_height (float): the height of the branches on the tree.
		_num_picked (int): the amount of fruit picked (starts at 0, maxes out at 4).
	"""
	_fruit_color: Signature
	_height: float
	_num_picked: int

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
	"""
	Represents the orchard, and contains all the trees.

	Params:
		_trees (List[List[Tree]]): a 2D array of the trees, with a higher-value index representing a tree farther away from origin.
	"""
	_trees: List[List[Tree]]

	def __init__(self) -> None:
		self._trees = [[], [], []]

	def _at_location(self, location: tuple[int, int]):
		return self._trees[location[0]][location[1]]
	
	def new_tree_discovered(self, location: tuple[int, int]) -> bool:
		"""
		Checks if a tree in a given location has been logged.

		Params:
			location (tuple[int, int]): the location of the tree to check.

		Returns:
			bool: true if a tree is not found at the location, false otherwise.
		"""
		return not self._at_location(location)

	def add_tree(self, color: Signature, height: float, location: tuple[int, int]) -> bool:
		"""
		Adds a tree to the orchard, if the tree has not already been logged.

		Params:
			color (Signature): the color of the fruits on the tree.
			height (float): the height of the branches on the tree.
			location (tuple[int, int]): the location of the tree.

		Returns:
			bool: true if successful (the tree is not already logged).
		"""
		if not self.new_tree_discovered(location):
			return False
		self._trees[location[0]][location[1]] = Tree(color, height)
		self._fill_third_tree(location[0])
		return True
	
	def get_tree_color(self, location: tuple[int, int]) -> Signature:
		return self._at_location(location).get_fruit_color()
			
	def get_tree_height(self, location: tuple[int, int]) -> float:
		return self._at_location(location).get_height()
	
	def _fill_third_tree(self, row: int) -> None:
		"""
		If two of the three trees in a row are logged, the third can be calculated

		Params:
			row (int): The row of trees to check.
		"""
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
