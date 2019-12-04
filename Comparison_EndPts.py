'''
Part of Final Project
Author: Prabhjot Kaur
'''
import copy
from Grid_Solver_2 import Grid

class Compare():
	'''
	This class compares if an end point
	is reoved from the list the distance or the time
	to reach all the end points in the list decrease by
	how much and for removal of which point this
	reduction is highest
	'''

	def __init__(self, grid, path_followed, start_pt, end_pt):
		self.grid = grid
		self.path = path_followed
		self.start = start_pt
		self.end = end_pt

	def max_reduce(self):
		min_path_len = len(self.path)
		ele_min_path = None
		for ele in self.end:
			start_pt = self.start
			end_list = copy.deepcopy(self.end)
			end_list.remove(ele)
			path_followed = []
			MAXITER = len(end_list) + 1
			ITER = 0
			while len(end_list) != 0:
				grid = Grid(self.grid, start_pt, end_list)
				new_origin, path_followed_new = grid.shortest_path()
				path_followed += list(reversed(path_followed_new))
				start_pt = new_origin
				ITER += 1
			if len(path_followed) < min_path_len:
				min_path = path_followed
				min_path_len = len(path_followed)
				ele_min_path = ele

		actual_path_len = len(self.path)
		reduction = ((actual_path_len - min_path_len) / actual_path_len)*100

		return(ele_min_path, reduction, min_path)


if __name__ == "__main__":
	pass