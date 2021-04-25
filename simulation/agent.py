from simulation.geometry import Point, Rectangle
import math
import copy


class Agent():
    def __init__(
            self,
            arena: Rectangle,
            speed: float,
            theta: float,
            pos: Point,
            can_be_on_fire: bool,
            encoding: str):
        self.__base_speed = speed
        self.__current_speed = speed
        self.__current_position = pos
        self.__direction_theta = theta
        self.__arena_rect = arena
        self.__can_be_on_fire = can_be_on_fire
        self.__encoding = encoding

    def position(self):
        return self.__current_position

    def rebound(self):
        self.__direction_theta = self.__arena_rect.rebound(
            self.__current_position, self.__direction_theta)

    def color(self):
        return [0, 0, 0]

    def is_position_on_fire(self, pattern, pos):
        # position range from -width/2 to +width/2, -height/2 to +height/2
        # numpy range from 0 to width and from 0 to height
        transformed_position = self.__current_position + \
            Point(self.__arena_rect.width() / 2, self.__arena_rect.height() / 2)
        index_x = min(int(transformed_position.x()),
                      self.__arena_rect.width() - 1)
        index_y = min(int(transformed_position.y()),
                      self.__arena_rect.height() - 1)

        return pattern[index_x, index_y]

    def update(self, fire_pattern):
        new_pos = copy.copy(self.__current_position)
        new_pos.update(
            self.__current_speed, self.__direction_theta)

        if self.__can_be_on_fire or not self.is_position_on_fire(
                fire_pattern, new_pos):
            self.__current_position = new_pos
        else:
            self.__current_speed = 0  # stop at the fire boundary

        if not self.__arena_rect.contains(self.__current_position):
            self.rebound()
