import enum
import random

# Globals
CELL_BURN_RATE = 10
FIRE_TRANSMISSION_PROBABILITY = 0.3

# Colours:
# ON_FIRE = yellow = (255, 255, 0)
# BURNT_OUT = black = (0, 0, 0)
# BURNABLE = -- a shade of green, proportional to burn -- = Cell.fuel * (0, 255, 0)  [light to dark as fuel is used up]
# TRENCH = lilac = (255, 0, 255)

class CellState(enum.Enum):
    BURNABLE = 1
    ON_FIRE = 2
    BURNT_OUT = 3
    TRENCH = 4

class Cell():
    # coords are the coordinates of the cell in the array - (x,y) from (0,0) = bottom left.
    # Remember that the coordinate system is ...#TODO [from top-left? which way is +ve x and +ve y?]
    def __init__(self, coords):
        self.__coords = coords
        self.__state = CellState.BURNABLE   # State of cell.
        self.__num_agents = 0   # Number of agents in cell.
        self.__fuel = 100   # %
    
    # fire_grid is the 2D list containing the Cells.
    # world_dims = (width, height)
    def update(self, fire_list_current, fire_list_next, fire_grid, world_dims):
        if not self.burn():     # Burning reduces remaining fuel.
            # If cell burnt out, remove from list.
            # TODO Improvement: don't like modifying this from inside this function.
            # This should perhaps be passed back and taken care of by the calling code.
            fire_list_next.append(self.__coords)
        
        # We already know that the cell is on fire.
        for neighbour_coord in self.get_neighbours(world_dims):
            neighbour = fire_grid[neighbour_coord[0]][neighbour_coord[1]]
            if neighbour.get_state() == CellState.BURNABLE:
                # Stochasticity
                if (random.random() >= (1 - FIRE_TRANSMISSION_PROBABILITY)):
                    # TODO Improvement: don't like modifying these from inside this function.
                    # These should perhaps be passed back and taken care of by the calling code.
                    neighbour.set_state(CellState.ON_FIRE)
                    fire_list_next.append(neighbour_coord)
    
    def get_neighbours(self, world_dims):
        neighbours = []
        
        # Manhattan distance of 1.
        for (i,j) in [(-1,0), (1,0), (0,-1), (0,1)]:
            (neighbour_x, neighbour_y) = (self.__coords[0] + i, self.__coords[1] + j)
            if (0 <= neighbour_x < world_dims[0]) and (0 <= neighbour_y < world_dims[1]):
                neighbours.append((neighbour_x, neighbour_y))
        
        return neighbours
    
    # Returns True if the cell has burnt out.
    def burn(self):
        self.__fuel = max(0, self.__fuel - CELL_BURN_RATE)    # E.g. burn rate = 10 (%) => tree burns out in 10 iterations.

        if self.__fuel == 0:
            self.__state = CellState.BURNT_OUT
            return True
        else:
            return False 
    
    def get_state(self):
        return self.__state
    
    def set_state(self, state):
        self.__state = state
    
    def get_coords(self):
        return self.__coords
    
    def get_remaining_fuel(self):
        return self.__fuel
    
    def add_one_agent(self):
        self.__num_agents = self.__num_agents+1
    
    def remove_one_agent(self):
        self.__num_agents = self.__num_agents-1
    
    def get_num_agents(self):
        return self.__num_agents