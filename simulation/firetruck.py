import numpy as np
from simulation import agent
from simulation.geometry import Point, Rectangle



class FireTruck(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: int):

        speed = 100  # km/h
        speed = speed * 3600 / 1000
        max_capacity = 7600  # liters https://en.wikipedia.org/wiki/Fire_engine#Water_tender

        super().__init__(arena, speed, theta, pos, False, max_capacity, encoding)
        self._current_liters = self._max_capacity


    def color(self):
        return [0, 0, 1]

    def put_out_fire(self, fire_pattern):
        fire_hose_length = 15 # meters https://en.wikipedia.org/wiki/Fire_hose
        
        directions_to_put_out = np.array([[0,0],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]])
        (index_x, index_y) = super().index_in_grid(super().position())

        positions_to_put_out = directions_to_put_out + [index_x,index_y]

        for [posx,posy] in positions_to_put_out :
            if 0<=posx<fire_pattern.shape[0] and  0<=posy<fire_pattern.shape[1]:
                if self._current_liters > 0 :
                    if fire_pattern[posx,posy] == 1:
                        fire_pattern[posx,posy] = 0
                        self._current_liters = max(0, self._current_liters-self._drop_rate) 
            

    def update(self, fire_pattern):
        super().update(fire_pattern)
        if self._current_liters > 0 :
            if self._current_speed == 0:
                self._current_speed = 1
                self.put_out_fire(fire_pattern)
            else :
                pass
                # Go towards fire
        
        else: 
            super().go_to_refill()


    def agent_type(self):
        return agent.Type.TRUCK