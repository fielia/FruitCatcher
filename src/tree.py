from vex import *

class FruitColor:
	"""
	An enum to better access the colors.

	Params:
			_sensitivity (float): the sensitivity value for each color.
	"""

	_sensitivity: float = 4.5
	LIME: Signature = Signature(1, -6935, -5887, -6410, 583, 2277, 1430, 4.5, 0)
	LEMON: Signature = Signature(2, -1547, -1001, -1274, -2479, -719, -1598, 4.5, 0)
	ORANGE_FRUIT: Signature = Signature(3, 2907, 4031, 3468, 961, 2563, 1762, 4.5, 0)
	GRAPEFRUIT: Signature = Signature(4, 6513, 7443, 6978, 1111, 1431, 1271, _sensitivity, 0)

possible_heights: list[float] = [17, 29, 38]
class Tree:
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

	def __init__(self) -> None:
		self._height = 0
		self._num_picked = 0

	def get_fruit_color(self) -> Signature:
		return self._fruit_color
	
	def set_fruit_color(self, new_color: Signature) -> None:
		self._fruit_color = new_color

	def get_height(self) -> float:
		return self._height
	
	def set_height(self, new_height: float) -> None:
		self._height = new_height

	def picked_one(self) -> None:
		self._num_picked += 1

	def get_picked(self) -> int:
		return self._num_picked
	
	def exists(self) -> bool:
		return self._height != 0


class Orchard:
	"""
	Represents the orchard, and contains all the trees.

	Params:
			_trees (List[List[Tree]]): a 2D array of the trees, with a higher-value index representing a tree farther away from origin.
	"""

	_trees: List[List[Tree]]

	def __init__(self) -> None:
		self._trees = [[Tree(), Tree(), Tree()], [Tree(), Tree(), Tree()], [Tree(), Tree(), Tree()]]

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
		return not self._at_location(location).exists()

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
		self._fill_colors(location[0], color)
		self._at_location(location).set_height(height)
		self._fill_third_tree(location[0])
		return True

	def get_tree_color(self, location: tuple[int, int]) -> Signature:
		if self._at_location(location):
			return self._at_location(location).get_fruit_color()
		raise Exception("Error: Tree at location " + str(location) + " not found. Query Variable: Color.")

	def get_tree_height(self, location: tuple[int, int]) -> float:
		if self._at_location(location).get_height() != 0:
			return self._at_location(location).get_height()
		raise Exception("Error: Tree at location " + str(location) + " not found. Query Variable: Height.")

	def _fill_colors(self, row: int, color: Signature) -> None:
		for tree in self._trees[row]:
			if not tree.exists():
				tree.set_fruit_color(color)

	def _fill_third_tree(self, row: int) -> None:
		"""
		If two of the three trees in a row are logged, the third can be calculated

		Params:
				row (int): The row of trees to check.
		"""
		if (
			not self._at_location((row, 0)).get_height() != 0
			and self._at_location((row, 1)).get_height() != 0
			and self._at_location((row, 2)).get_height() != 0
		):
			fruit_height: float = 0
			for height in possible_heights:
				if (
					not self._at_location((row, 1)).get_height() == height
					and not self._at_location((row, 2)).get_height() == height
				):
					fruit_height = height
			self._trees[row][0].set_height(fruit_height)

		elif (
			self._at_location((row, 0)).get_height() != 0
			and not self._at_location((row, 1)).get_height() != 0
			and self._at_location((row, 2)).get_height() != 0
		):
			fruit_height: float = 0
			for height in possible_heights:
				if (
					not self._at_location((row, 2)).get_height() == height
					and not self._at_location((row, 0)).get_height() == height
				):
					fruit_height = height
			self._trees[row][1].set_height(fruit_height)

		elif (
			self._at_location((row, 0)).get_height() != 0
			and self._at_location((row, 1)).get_height() != 0
			and not self._at_location((row, 2)).get_height() != 0
		):
			fruit_height: float = 0
			for height in possible_heights:
				if (
					not self._at_location((row, 0)).get_height() == height
					and not self._at_location((row, 1)).get_height() == height
				):
					fruit_height = height
			self._trees[row][2].set_height(fruit_height)
