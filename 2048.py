"""
Clone of 2048 game.
"""
import gui
import random 
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}
#merge I stole from Benjamin Shieh because it's awesome :)
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    merged_line = [0] * len(line)
    merge_idx = 0
    for value in line:
        if value:
            if not(merged_line[merge_idx]):
                merged_line[merge_idx] = value
            elif value - merged_line[merge_idx]:
                merge_idx+=1
                merged_line[merge_idx] = value                   
            else:
                merged_line[merge_idx] *= 2
                merge_idx+=1               
    return merged_line             

#old merge
#def merge(line):
#    results = filter(None, line)
#    
#    for dummy_i in xrange(len(results)-1):
#        try:
#            if results[dummy_i+1] == results[dummy_i]:
#                results[dummy_i] *= 2 
#                results.pop(dummy_i+1)
#        except IndexError: break
#    return results + [0] * (len(line)-len(results))


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # initialize obj attributes
        self._height = grid_height
        self._width = grid_width
        #game over stuff
        self._message=''
        self._coordinates = [(row,col)for row in xrange(self._height)
                             for col in xrange(self._width)]
        self._neighbour_offsets = [(0,1),(0,-1),(1,0),(-1,0)]
        #victory!
        self._grid_values = []
        self._continued = False
        self._2048 = False
        #history for undo
        self._move_index = 0
        self._move_history = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[],
                             8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[]}
        #set step lists
        self._grid= []
        self._two_four = [2,2,2,2,2,2,2,2,2,4]                                  
        self._direction_indices = {}
        self._direction_indices[UP] = [(0, col) for col in xrange(self._width)]
        self._direction_indices[DOWN] = [(self._height - 1, col) for col in
                                       xrange(self._width)]
        self._direction_indices[LEFT] = [(row, 0) for row in
                                         xrange(self._height)]
        self._direction_indices[RIGHT] = [(row, self._width - 1) for row in
                                          xrange(self._height)]
        self._direction_length = {UP:self._height, DOWN:self._height,
                                  LEFT:self._width, RIGHT:self._width}
        # call to reset method to start new game
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        
        self._continued = False
        self._message = ''
        self._two_four[9] = 4
        self._2048 = False
        self._move_index = 0
        self._move_history = {0:[], 1:[], 2:[], 3:[],
                              4:[], 5:[], 6:[], 7:[],
                              8:[], 9:[], 10:[], 11:[],
                              12:[], 13:[], 14:[]}
        self._grid = [[0 for dummy_i in xrange(self._width)]
                     for dummy_i in xrange(self._height)]
        
        self.new_tile()
        self.new_tile()
        self._move_history[(self._move_index%15)] = [[self.get_tile(row, col)
                                                      for col in
                                                      xrange(self._width)]
                                                   for row in
                                                   xrange(self._height)]
        
    def reset_2048_mode(self):
        
        self.reset()
        self._two_four[9] = 2048
        self._2048 = True
        self._continued = True
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._width
    
    def game_over(self):
        #iterates through a list of grid coordinate tuples
        #usings self._neighbour_offsets [(0,1),(0,-1),(1,0),(-1,0)]
        #to check neighbours  
        #returns True for 0's and neighbouring pairs or game over
        for cord in self._coordinates:
            for offset in self._neighbour_offsets:
                if 0 <= cord[0] + offset[0] < self._height:
                    if 0 <= cord[1] + offset[1] < self._width:
                        if (self.get_tile(cord[0]+offset[0],
                                cord[1]+offset[1]) == 0):
                            return False
                        
                        if (self.get_tile(cord[0], cord[1]) ==
                              self.get_tile(cord[0] + offset[0],
                                          cord[1] + offset[1])):
                            return False
        return True
    
    def have_2048(self):
        if 2048 in [self.get_tile(tile[0], tile[1])
                    for tile in self._coordinates]:
            self._2048 = True
            return True
        
    def get_message(self):
        return self._message
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        changed=False
        for index in self._direction_indices[direction]:
            line_indices = [(index[0] + step * OFFSETS[direction][0], 
                           index[1] + step * OFFSETS[direction][1]) 
                           for step in
                           xrange(self._direction_length[direction])]
                
            line_values = [self.get_tile(index[0], index[1])
                           for index in line_indices]
            
            merged_line = merge(line_values)
            
            if merged_line != line_values:
                for num in xrange(self._direction_length[direction]):
                    self.set_tile(line_indices[num][0],
                                  line_indices[num][1],
                                  merged_line[num])
                    changed = True
             
        if changed:
            self.new_tile()
            self._move_index += 1
            self._move_history[(self._move_index%15)] = [[
                          self.get_tile(row, col) 
                          for col in xrange(self._width)] 
                          for row in xrange(self._height)]
    
        if self.game_over():
            self._message = 'Game Over'
#            print 'Game Over'

        if not self._continued:
            if self.have_2048():
                self._message = '2048!' 
#        print self._move_history

    def undo(self):
        #if (self._move_index%15)  > 0:
        previous_grid = self._move_history[(self._move_index%15)-1]

        for cord in self._coordinates:
            self.set_tile(cord[0],cord[1],previous_grid[cord[0]][cord[1]])
        self._move_index -= 1

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #Creates list of empty tiles
        empty_tiles = [(row,col) for row in xrange(self.get_grid_height())
                      for col in xrange(self.get_grid_width()) 
                      if not self.get_tile(row,col)]

        new_tile = random.choice(empty_tiles)
        self.set_tile(new_tile[0],new_tile[1],random.choice(self._two_four))
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

gui.run_gui(TwentyFortyEight(4,4))



