import math

from simulation import agent
from simulation.geometry import Point, Rectangle
import numpy as np
import sys



class Drone(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: int):

        speed = 45  # km/h
        speed = speed * 3600 / 1000  # m/s
        max_capacity = 150 # liters
        super().__init__(arena, speed, theta, pos, True, max_capacity, encoding)
        self._current_liters = self._max_capacity
        
        self.__state = None

    def color(self):
        return [0, 1, 0]

    def should_drop_water(self, fire_pattern):
        # This is modified by the encoding
        if self.count_positions_on_fire(fire_pattern) > int(self._encoding):
            return True 
        else:
            return False

    def count_positions_on_fire(self,fire_pattern):
        (index_x, index_y) = super().index_in_grid(super().position())
        x_start = max(0, index_x-1)
        x_end = min(fire_pattern.shape[0]-1, index_x+1)
        y_start = max(0, index_y-1)
        y_end = min(fire_pattern.shape[0]-1, index_y+1)
        
        positions_on_fire = np.sum(fire_pattern[x_start:x_end,y_start:y_end])
        return positions_on_fire
        

    def agent_type(self):
        return agent.Type.DRONE
    
    def update_direction(self, fire_pattern):
        (index_x, index_y) = super().index_in_grid(super().position())
        # Assume that the temperature sensor would detect high temperature up
        # to 10 meters away in any direction
        drone_range = 10
        (start_x, start_y) = (max(0, index_x - drone_range),
                              max(0, index_y - drone_range))
        (end_x,
         end_y) = (min(fire_pattern.shape[0],
                       index_x + drone_range),
                   min(fire_pattern.shape[1],
                       index_y + drone_range))
        detected_area = fire_pattern[start_x:end_x, start_y:end_y]
        if detected_area.any():
            detected_indices = np.argwhere(detected_area == 1)
            center_point = (
                detected_area.shape[0] / 2.,
                detected_area.shape[1] / 2.)
            closest_index = np.argmin(detected_indices - center_point)
            direction = closest_index - center_point
            self._direction_theta = math.atan2(direction[1], direction[0])

        return

    def update(self, fire_pattern):
        super().update(fire_pattern)

        # Drone strategy :
        if self._current_liters > 0:  # if have water
            if self.should_drop_water(fire_pattern):  # drop
                self.__state = agent.State.ON_FIRE
                (index_x, index_y) = super().index_in_grid(super().position())
                fire_pattern[index_x, index_y] = 0
                self._current_liters = max(
                    0, self._current_liters - self._drop_rate)
                self._current_speed = 1
            else:  # go to fire
                self.update_direction(fire_pattern)
                self.__state = agent.State.GOING_TO_FIRE
                self._current_speed = self._base_speed

        else:  # go to water tank location
            super().go_to_refill()
