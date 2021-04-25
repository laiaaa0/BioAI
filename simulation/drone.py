from simulation import agent
from simulation.geometry import Point, Rectangle


class Drone(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: str):

        speed = 45
        super().__init__(arena, speed, theta, pos, True, encoding)

    def color(self):
        return [0, 1, 0]
