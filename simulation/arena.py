from simulation.firefighter import Firefighter
from simulation.drone import Drone
from simulation.firetruck import FireTruck
from simulation.geometry import Rectangle, Point
from simulation.cell import *
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import enum
import itertools


class Arena():
    # init_fire is an array of 2-tuples specifying the initial cells which are on fire: [(x1,y1), (x2,y2)].
    def __init__(self, init_fire_cells, num_agents=5):
        self.__width = 100  # m (1 km)
        self.__height = 100  # m (1 km) - each pixel is 1 m2
        self.__rectangle = Rectangle(0,0, self.__width, self.__height)
        # Keeps track of the cells on fire, so that it doesn't have to check all of the cells in the grid on every iteration.
        # List of cell coordinates.
        self.__on_fire = []
        self.__agent_list = []

        self.initialise_agents(num_agents)
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, aspect='equal')
        self.__ax.set_autoscale_on(False)
        self.__ax.axis([0, self.__width, 0, self.__height])

        # Create grid - 2D array of Cell objects.
        # Coordinate system aligns with axes - bottom left is (0,0).
        self.__fire_grid = [[Cell((j,i)) for i in range(self.__width)] for j in range(self.__height)]

        # 'Start' fire at given coordinates
        self.initialise_fire(init_fire_cells)

        # Testing
        '''
        print(self.__fire_grid[0][0].get_coords())
        print(self.__fire_grid[99][0].get_coords())
        print(self.__fire_grid[0][99].get_coords())
        print(self.__fire_grid[99][99].get_coords())
        '''

        # From previous version
        '''
        self.__pattern = np.zeros(
            (self.__width, self.__height), dtype=np.uint8)
        
        self.__pattern[int(self.__width /
                           3):int(2 *
                                  self.__width /
                                  3), int(self.__height /
                                          3):int(2 *
                                                 self.__height /
                                                 3)] = 1
                                                 '''
    
    def initialise_fire(self, init_fire_cells):
        for x, y in init_fire_cells:
            self.__fire_grid[x][y].set_state(CellState.ON_FIRE)
            self.__on_fire.append((x, y))

    def initialise_agents(self, num_agents: int, seed=42):
        random.seed(seed)
        for i in range(num_agents):
                self.__agent_list.append(
                    Firefighter(
                        self.__rectangle,
                        theta=random.uniform(
                            0,
                            2 * math.pi),
                        pos=self.__rectangle.random_point_int(seed),
                        encoding=0))
    
    def add_trench(self, trench_coords):
        for x, y in trench_coords:
            self.__fire_grid[x][y].set_state(CellState.TRENCH)

    def extinguish(self, extinguish_coords):
        for x, y in extinguish_coords:
            if self.__fire_grid[x][y].get_state() == CellState.ON_FIRE:
                self.__fire_grid[x][y].set_state(CellState.BURNABLE)

    def image_from_pattern(self):
        coloured_pattern = np.ones(
            (self.__width, self.__height, 4), dtype=np.uint8) * 255
        
        for x, y in itertools.product(range(self.__width), range(self.__height)):
            fire_cell = self.__fire_grid[x][y]
            if fire_cell.get_state() == CellState.ON_FIRE:
                # yellow
                coloured_pattern[x, y, 2] = 0
            elif fire_cell.get_state() == CellState.BURNT_OUT:
                # black
                coloured_pattern[x, y, 0] = 50
                coloured_pattern[x, y, 1] = 50
                coloured_pattern[x, y, 2] = 50
            elif fire_cell.get_state() == CellState.BURNABLE:
                # colour green proportional to amount of fuel remaining
                coloured_pattern[x, y, 0] = 0
                coloured_pattern[x, y, 1] = 255 * fire_cell.get_remaining_fuel() / 100
                coloured_pattern[x, y, 2] = 0
            elif fire_cell.get_state() == CellState.TRENCH:
                # lilac
                coloured_pattern[x, y, 1] = 0

        img = Image.fromarray(coloured_pattern, mode="RGBA")
        return img

    def update(self):

        # Gets populated during the iteration
        for agent in self.__agent_list:
            agent.update(self.__fire_grid)

        on_fire_next_itr = []
        for x, y in self.__on_fire:
            self.__fire_grid[x][y].update(self.__on_fire, on_fire_next_itr, self.__fire_grid, (self.__width, self.__height))
        
        self.__on_fire = on_fire_next_itr

    def plot(self):
        self.__ax.cla()
        x = [a.position().x() for a in self.__agent_list]
        y = [a.position().y() for a in self.__agent_list]
        colors = [a.color() for a in self.__agent_list]
        self.__ax.scatter(x, y, c=colors)
        self.__ax.axis([0, self.__width , 0, self.__height])
        self.__ax.imshow(self.image_from_pattern(), extent=(self.__ax.axis()))
        plt.pause(0.03)

# Testing
if __name__ == "__main__":
    a = Arena()