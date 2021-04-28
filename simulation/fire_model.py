# General thoughts:
#   For report: swarms, neural nets, evolutionary algorithms, cellular automata + sympathetic bio-inspired sensors with swarm networking.
#   [IMPORTANT] One thought - controllers have to be human readable/explainable to form strategies which humans are able to follow?

import numpy as np
from simulation.arena import Arena
import matplotlib.pyplot as plt

'''
 Design:
  o Will calculate next fire state whenever Arena.update() is called. 
'''

class FireModel():
    '''
     prevailing_wind - 2D numpy vector. Magnitude (norm) of vector gives wind speed in ms^-1. 
     init_fire - list of 2-tuples: [(x1,y1), (x2,y2), ...]
    '''
    def __init__(self, prevailing_wind, init_fire):
        self.__wind_speed = np.linalg.norm(prevailing_wind)
        self.__wind_dir = prevailing_wind / self.__wind_speed   # Normalise to unit vector

        # Set up world
        self.__fire_grid = Arena()
        # Using temporary methods added to Arena class.
        self.__pattern_width, self.__pattern_height = self.__fire_grid.get_dims()
        self.__fire_grid.remove_agents()
        self.__fire_grid.clear_pattern()
        self.__fire_grid.set_pattern(init_fire)

        # TODO Still need to model (check the realism of these aspects):
        #  o Still need to incorporate prevailing wind into model.
        #  o Burnout (+ Model amount of fuel - each square could have a time for which it is able to burn.
        #    After the limit has been reached, the tree will stop burning?)
        #  o Gradient of slope.
    
    # How can this be made more efficient? I.e. just expand at the boundary (note: how would this work regarding
    # the fire burning out from the middle)? Don't really want to consider every square every time.
    def update(self):
        # Testing
        #print("(20,20): {}, (20,21): {}.".format(self.__fire_grid.on_fire(self.__fire_grid.axis_to_pattern((20,20))), self.__fire_grid.on_fire(self.__fire_grid.axis_to_pattern((20,21)))))
        
        # Set alight based on neighbours.
        # Create a copy of the array for the next time step.
        fire_advanced = np.copy(self.__fire_grid.get_pattern())
        # TODO A little disorientated about which way is width and which is height!
        for i in range(1, self.__pattern_width - 1):
            for j in range(1, self.__pattern_height - 1):
                if self.__fire_grid.on_fire((i,j)):
                    self.spread_to_neighbours(fire_advanced, (i,j))
        self.__fire_grid.overwrite_pattern(fire_advanced)
        #pass
    
    # Helper method for update
    def spread_to_neighbours(self, new_fire_grid, pattern_coord):
        # Spread fire by Manhattan distance of 1.
        for (i,j) in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]:
            new_fire_grid[pattern_coord[0] + i, pattern_coord[1] + j] = 1
    
    def plot(self):
        self.__fire_grid.plot()


# Testing
if __name__ == "__main__":
    #print("Executing as main.")

    num_iterations = 30
    
    # Start fire
    # Initial wind and fire:
    wind = np.array([3,3])
    init_fire = [(0,0), (20,20), (50,50), (50,51)]
    fire_model = FireModel(wind, init_fire)

    #for i in range(num_iterations):
    while True:
        fire_model.update()
        fire_model.plot()
        print("Updated plot")
    plt.show()