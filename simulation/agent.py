from simulation.geometry import Point, Rectangle
import math


class Habituation():
    def __init__(self, frames: int):
        self.__is_habituated = False
        self.__frames_since_change = 0
        self.__frames_to_habituate = frames

    def reset(self):
        self.__is_habituated = False
        self.__frames_since_change = 0

    def increase(self):
        self.__frames_since_change = self.__frames_since_change + 1
        if self.__frames_since_change > self.__frames_to_habituate:
            self.__is_habituated = True

    def is_habituated(self):
        return self.__is_habituated


class Agent():
    def __init__(
            self,
            arena: Rectangle,
            speed: float,
            theta: float,
            pos: Point):
        self.__base_speed = speed
        self.__current_speed = speed
        self.__current_position = pos
        self.__direction_theta = theta
        self.__arena_rect = arena

    def position(self):
        return self.__current_position

    def rebound(self):
        self.__direction_theta = self.__arena_rect.rebound(
            self.__current_position, self.__direction_theta)

    def update(self, on_fire: bool):
        self.__current_position.update(
            self.__current_speed, self.__direction_theta)
        if not self.__arena_rect.contains(self.__current_position):
            self.rebound()
