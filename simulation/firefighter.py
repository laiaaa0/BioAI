from simulation import agent
from simulation.geometry import Point, Rectangle


class Firefighter(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            speed: float,
            theta: float,
            pos: Point,
            encoding: str):
        super().__init__(arena, speed, theta, pos, encoding)

    def color(self):
        return [1, 0, 0]
