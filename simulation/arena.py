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
        self.__width = 1000
        self.__height = 1000
        self.__rectangle = Rectangle(-self.__width / 2, -
                                     self.__height / 2, self.__width, self.__height)
        self.__agent_list = []
        self.initialise_agents(num_agents)
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, aspect='equal')
        self.__ax.set_autoscale_on(False)
        self.__ax.axis([-self.__width / 2, self.__width /
                        2, -self.__height / 2, self.__height / 2])

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
            if i % 3 == 0:
                self.__agent_list.append(
                    Firefighter(
                        self.__rectangle,
                        theta=random.uniform(
                            0,
                            2 * math.pi),
                        pos=self.__rectangle.random_point(seed),
                        encoding=""))
            elif i % 3 == 1:
                self.__agent_list.append(
                    Drone(
                        self.__rectangle,
                        theta=random.uniform(
                            0,
                            2 * math.pi),
                        pos=self.__rectangle.random_point(seed),
                        encoding=""))
            else:

                self.__agent_list.append(
                    FireTruck(
                        self.__rectangle,
                        theta=random.uniform(
                            0,
                            2 * math.pi),
                        pos=self.__rectangle.random_point(seed),
                        encoding=""))

    def image_from_pattern(self):
        coloured_pattern = np.ones(
            (self.__width, self.__height, 4), dtype=np.uint8) * 255
        coloured_pattern[:, :, 2] = 0
        coloured_pattern[:, :, 3] = self.__pattern * 255
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
        self.__ax.axis([-self.__width / 2, self.__width /
                        2, -self.__height / 2, self.__height / 2])
        self.__ax.imshow(self.image_from_pattern(), extent=(self.__ax.axis()))
        plt.pause(0.05)
