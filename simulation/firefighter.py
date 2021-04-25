from simulation import agent
from simulation.geometry import Point, Rectangle


class Firefighter(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: str):
        speed = 5  # km/h
        speed = speed * 3600 / 1000  # m/s
        super().__init__(arena, speed, theta, pos, False, 0,encoding)

    def color(self):
        return [1, 0, 0]
