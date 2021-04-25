import math

from simulation import agent
from simulation.geometry import Point, Rectangle
import enum
import numpy as np
import sys


class DroneState(enum.Enum):
    GOING_TO_REFILL = 1
    GOING_TO_FIRE = 2
    ON_FIRE = 3


class Drone(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: str):

        speed = 45  # km/h
        speed = speed * 3600 / 1000  # m/s
        super().__init__(arena, speed, theta, pos, True, encoding)
        self.__water_tank_location = Point(400, 400)
        self.__max_capacity = 150  # liters
        self.__current_liters = self.__max_capacity
        # Liters/m^2 (https://bedtimemath.org/fun-math-firefighting/)
        self.__drop_rate = 17
        self.__state = None

    def color(self):
        water_tank_percentage = self.__current_liters / \
            float(self.__max_capacity)
        if self.__state:
            if self.__state == DroneState.GOING_TO_FIRE:
                return [0, 1, 1]
            else:
                return [0, 1, 0]
        return [0, 0, 0]

    def should_drop_water(self, fire_pattern):
        # This is modified by the encoding
        return super().is_position_on_fire(fire_pattern, super().position())

    def update_direction(self, fire_pattern):
        # This is modified by encoding
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
        if self.__current_liters > 0:  # if have water
            if self.should_drop_water(fire_pattern):  # drop
                self.__state = DroneState.ON_FIRE
                (index_x, index_y) = super().index_in_grid(super().position())
                fire_pattern[index_x, index_y] = 0
                self.__current_liters = max(
                    0, self.__current_liters - self.__drop_rate)
                self._current_speed = 1
            else:  # go to fire
                self.update_direction(fire_pattern)
                self.__state = DroneState.GOING_TO_FIRE
                self._current_speed = self._base_speed

        else:  # go to water tank location
            direction = self.__water_tank_location - super().position()
            if direction.norm() < 5:  # refill
                self.__current_liters = self.__max_capacity
            else:
                self._direction_theta = math.atan2(
                    direction.y(), direction.x())
                self.__state = DroneState.GOING_TO_REFILL
                self._current_speed = min(self._base_speed, direction.norm())
