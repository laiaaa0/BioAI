from simulation import agent
from simulation.geometry import Point, Rectangle


class FireTruck(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: str):

        speed = 100
        super().__init__(arena, speed, theta, pos, encoding)

    def color(self):
        return [0, 0, 1]
