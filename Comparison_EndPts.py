'''
Part of Final Project - Comparison of paths if an end point is removed
Author: Prabhjot Kaur
This code was written in order to see that if any of the endpoint is removed
from the list lets say that if we want to know that we aren't wasting time and
fuel in just going to a point which is really far from the others. In this case
maybe some other vehicle can be used to drop in all points in that area.
This function calculates the minimum path length so found by the removal of a
specific end point. Then it calculates the reduction percentage when comparing
to original path.
'''
import copy
from Grid_Solver_2 import Grid


class Compare():
    '''
    This class compares if an end point
    is removed from the list the distance or the time
    to reach all the end points in the list decreases by
    how much and for removal of which point this
    reduction is highest
    '''

    def __init__(self, grid, path_followed, start_pt, end_pt):
        '''
        Initialises the Compare Class object

        ** Parameters **
        self : Object of Class
        grid : List of Lists : *int*
              Grid so generated from the image
        path_followed : List of tuples : *int*
             The path so followed to go from start point to
             all the end points
        start_pt : Tuple : *int*
            Start point so mentioned by the user
        end_pt : List of tuples : *int*
            List of all the end points mentioned by the user

        ** Returns **
        Nothing!
        '''
        self.grid = grid
        self.path = path_followed
        self.start = start_pt
        self.end = end_pt

    def max_reduce(self):
        '''
        This function is to find by the removal of which end point
        the path reduces the most and what is the percentage of reduction

        ** Parameters **
        None

        ** Returns **
        ele_min_path : Tuple : *int*
                  The end point whose removal reduces the path length the most
        reduction : *Float*
                  The percentage reduction in path caused by the removal of
                  this end point
        min_path : List of tuples : *int*
                 The shorter path so found by the removal of this end point
        '''

        min_path_len = len(self.path)
        ele_min_path = None

        for ele in self.end:
            start_pt = self.start
            end_list = copy.deepcopy(self.end)
            end_list.remove(ele)
            path_followed = []
            while len(end_list) != 0:
                grid = Grid(self.grid, start_pt, end_list)
                new_origin, path_followed_new = grid.shortest_path()
                path_followed += list(reversed(path_followed_new))
                start_pt = new_origin
            if len(path_followed) < min_path_len:
                min_path = path_followed
                min_path_len = len(path_followed)
                ele_min_path = ele

        actual_path_len = len(self.path)
        reduction = ((actual_path_len - min_path_len) / actual_path_len) * 100

        return(ele_min_path, reduction, min_path)


if __name__ == "__main__":
    pass
