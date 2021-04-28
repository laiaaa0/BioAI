from simulation.firefighter import Firefighter
from simulation.drone import Drone
from simulation.firetruck import FireTruck
from simulation.geometry import Rectangle, Point
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import enum


class Arena():
    def __init__(self, num_agents=5):
        self.__width = 100  # m (1 km)
        self.__height = 100  # m (1 km) - each pixel is 1 m2
        self.__rectangle = Rectangle(0,0, self.__width, self.__height)
        self.__agent_list = []
        self.initialise_agents(num_agents)
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, aspect='equal')
        self.__ax.set_autoscale_on(False)
        self.__ax.axis([0, self.__width ,0, self.__height])

        self.__pattern = np.zeros(
            (self.__width, self.__height), dtype=np.uint8)
        
        self.__pattern[int(self.__width /
                           3):int(2 *
                                  self.__width /
                                  3), int(self.__height /
                                          3):int(2 *
                                                 self.__height /
                                                 3)] = 1

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

    def image_from_pattern(self):
        coloured_pattern = np.ones(
            (self.__width, self.__height, 4), dtype=np.uint8) * 255
        coloured_pattern[:, :, 2] = 0
        coloured_pattern[:, :, 3] = (self.__pattern==1) * 255
        img = Image.fromarray(coloured_pattern, mode="RGBA")
        return img

    def update(self):
        for agent in self.__agent_list:
            agent.update(self.__pattern)

    def plot(self):
        self.__ax.cla()
        x = [a.position().x() for a in self.__agent_list]
        y = [a.position().y() for a in self.__agent_list]
        colors = [a.color() for a in self.__agent_list]
        self.__ax.scatter(x, y, c=colors)
        self.__ax.axis([0, self.__width , 0, self.__height])
        self.__ax.imshow(self.image_from_pattern(), extent=(self.__ax.axis()))
        plt.pause(0.05)
    

    # Temp - added by FT for fire_model code.
    def remove_agents(self):
        self.__agent_list = []
    
    # Temp - added by FT for fire_model code.
    def get_dims(self):
        return [self.__width, self.__height]
    
    # Temp - added by FT for fire_model code.
    def clear_pattern(self):
        self.__pattern = np.zeros(
            (self.__width, self.__height), dtype=np.uint8)

    # Temp - added by FT for fire_model code.
    # coords is a list of coordinates to set to 1.
    def set_pattern(self, coords):
        for axis_coord in coords:
            pattern_coord = self.axis_to_pattern(axis_coord)
            self.__pattern[pattern_coord[0], pattern_coord[1]] = 1
    
    # Temp - added by FT for fire_model code.
    def overwrite_pattern(self, pattern):
        self.__pattern = pattern
    
    # Temp - added by FT for fire_model code.
    # Translates axis coords into pattern coords.
    def axis_to_pattern(self, axis_coord):
        # TODO Need to change this 99 to be __width or __height (which one?)
        return [99 - axis_coord[1], axis_coord[0]]
    
    # Temp - added by FT for fire_model code.
    def get_pattern(self):
        return self.__pattern

    # Temp - added by FT for fire_model code.
    def on_fire(self, pattern_coord):
        return self.__pattern[pattern_coord[0], pattern_coord[1]]
