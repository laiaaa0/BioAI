from simulation import agent
from simulation.geometry import Point, Rectangle


class Drone(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            speed: float,
            theta: float,
            pos: Point,
            encoding: str):
        super().__init__(arena, speed, theta, pos, encoding)

    def color(self):
        return [0, 1, 0]
