'''
Grid Solver Class
Prabhjot Kaur
'''
import queue
import sys
import copy

WALL = 0
PATH = 1
VALID_PATH = 2
INVALID_PATH = 3
ENDPOINT = 4
INTMAX = sys.maxsize - 1


class Grid:
    '''
    Consists of function to solve the grid
    i.e find the shortest path from origin to
    multiple drop points
    '''

    def __init__(self, grid, start_pt, end_pt):
        self.grid = grid
        self.h = len(grid)
        self.w = len(grid[0])
        self.follow = queue.Queue(INTMAX)
        self.path = queue.Queue(INTMAX)
        self.start = start_pt
        self.end = end_pt

    def shortest_path(self):
        '''
        Breadth for Search Algorithm
        '''
        possible_coord = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        visited_grid = [[ False for j in range(self.w)] for i in range(self.h)]
        end_pt = copy.deepcopy(self.end)
        # if the start and the end points are not a valid path
        if self.grid[self.start[0]][self.start[1]] != 1:
            for end in self.end:
                if self.grid[end[0]][end[1]] != 1:
                    return -1
        # Start point is now visited
        visited_grid[self.start[0]][self.start[1]] = True
        self.path.put(self.start)
        success = False
        # Looping through the VALID PATH
        while len(list(self.path.queue)) != 0:
            # accessing the first element of queue
            current_pos = self.path.queue[0]
            if current_pos in self.end:
                if current_pos not in self.follow.queue:
                    self.follow.put(current_pos)
                self.end.pop(self.end.index(current_pos))
                if len(self.end) == 0:
                    success = True
                    continue
                # return [True, list(self.follow.queue)]
            else:
                self.path.get()
                for i in range(len(possible_coord)):
                    next_x = current_pos[0] + possible_coord[i][0]
                    next_y = current_pos[1] + possible_coord[i][1]
                    if self.valid_point((next_x, next_y), self.h, self.w) and visited_grid[next_x][next_y] == False and self.grid[next_x][next_y] == 1:
                        visited_grid[next_x][next_y] = True
                        self.path.put((next_x, next_y))
                        if current_pos not in self.follow.queue:
                            self.follow.put(current_pos)
        # total_path = len(list(self.follow.queue))
        final_path = [list(self.follow.queue)[-1]]
        counter = 0
        if final_path[-1] not in end_pt:
            final_path = self.mod_finalpath(end_pt)
        for i, ele in enumerate(reversed(list(self.follow.queue))):
            x = ele[0]
            y = ele[1]
            n = self.follow.queue.index(ele)
            x2 = self.follow.queue[n - 1][0]
            y2 = self.follow.queue[n - 1][1]
            last_pos = final_path[counter]
            if ele not in final_path and (x == last_pos[0] and (y == last_pos[1] + 1 or y == last_pos[1] - 1)) or (y == last_pos[1] and (x == last_pos[0] + 1 or x == last_pos[0] - 1)):
                if (x2 == last_pos[0] and (y2 == last_pos[1] + 1 or y2 == last_pos[1] - 1)) or (y2 == last_pos[1] and (x2 == last_pos[0] + 1 or x2 == last_pos[0] - 1)) and (x2, y2) in end_pt:
                    final_path.append((x2, y2))
                    counter += 1
                else:
                    final_path.append(ele)
                    counter += 1
        return(success, final_path)

    def valid_point(self, coord, height, width):
        x = coord[0]
        y = coord[1]
        if x >= 0 and y >= 0 and x < height and y < width:
            return True
        else:
            return False

    def mod_finalpath(self, end_pt):
        for ele in list(reversed(self.follow.queue)):
            if ele in end_pt:
                index = list(self.follow.queue).index(ele)
                break
        final_path = [list(self.follow.queue)[index]]
        n = len(list(self.follow.queue))
        for i in range(n, -1, index + 1):
            final_path.append(list(self.follow.queue)[i])
        return(final_path)


if __name__ == "__main__":
    '''
    maze = [[1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 0, 0, 1], [0, 0, 1, 1, 1, 0, 1]
             , [0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 0, 0, 1], [0, 1, 1, 1, 0, 1, 1]
             , [0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 1, 1, 1]]
    start_pt = (0, 0)
    end_pt = [(1, 3), (3, 3), (7, 4), (0, 6)]
    grid = Grid(maze, start_pt, end_pt)
    result, path_followed = grid.shortest_path()
    if result:
        print("Congo")
        print("Path followed : ")
        print(list(reversed(path_followed)))
    else:
        print("Fail")
    maze = [[1, 0, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0], [0, 1, 1, 1]]
    start_pt = (0, 0)
    end_pt = [(1, 2), (2, 1)]
    grid = Grid(maze, start_pt, end_pt)
    result, path_followed = grid.shortest_path()
    if result:
        print("Congo")
        print("Path followed : ")
        print(list(reversed(path_followed)))
    else:
        print("Fail")
    '''