from simulation import agent
from simulation.geometry import Point, Rectangle
from simulation.cell import Cell, CellState
import enum 
import numpy as np
import random

class Action(enum.Enum):
    EXTINGUISH=1
    TRENCH=2
    BURN=3
    MOVE=4
    NONE=5

class Direction(enum.Enum):
    EAST = 1
    WEST = 2
    NORTH = 3
    SOUTH = 4
    NONE = 5
    
    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value

direction_list = np.array([[0,1],[0,-1],[1,0],[-1,0],[0,0]])
class Firefighter(agent.Agent):
    def __init__(
            self,
            arena: Rectangle,
            theta: float,
            pos: Point,
            encoding: int):
        speed = 5  # km/h
        speed = speed * 3600 / 1000  # m/s
        super().__init__(arena, speed, theta, pos, False, 0, encoding)
        self.direction = Direction.NONE
        self.alive = True

    def color(self):
        return [1, 0, 0]

    def agent_type(self):
        return agent.Type.FIGHTER


    def move(self,new_pos, terrain_map):
        terrain_map[self._current_position.x()][self._current_position.y()].remove_one_agent()
        self._current_position= new_pos
        terrain_map[self._current_position.x()][self._current_position.y()].add_one_agent()
    
    def do_action(self, dir:Direction, action, pattern):
        direction_value = direction_list[int(dir)-1]
        new_pos = self._current_position+Point(direction_value[0],direction_value[1])
        if self._arena_rect.contains(new_pos):
            if action == Action.EXTINGUISH:
                if pattern[new_pos.x()][new_pos.y()].get_state() == CellState.ON_FIRE:
                    pattern[new_pos.x()][new_pos.y()].set_state(CellState.BURNABLE)
            elif action == Action.MOVE:
                self.move(new_pos,pattern)
            elif action == Action.TRENCH:
                pattern[new_pos.x()][new_pos.y()].set_state(CellState.TRENCH)
            elif action == Action.BURN:
                pattern[new_pos.x()][new_pos.y()].set_state(CellState.ON_FIRE)
            else:
                pass

    def get_network_input(self, pattern):
        directions = np.array([[-1,1],[0,1],[1,1],[-1,0],[0,0],[1,0],[-1,-1],[0,-1],[1,-1]], dtype=np.int8)
        positions = [int(self._current_position.x()), int(self._current_position.y())]+directions
        inputs = []
        for [posx,posy] in positions:
            if self._arena_rect.contains(Point(posx,posy)):
                inputs.append(int(pattern[posx][posy].get_state()))
                inputs.append(int(pattern[posx][posy].get_num_agents()))                
            else:
                inputs.append(0)
                inputs.append(0)

        return inputs

    def update(self, fire_grid, net):
        if self.alive:
            if net:
                inputs = self.get_network_input(fire_grid)
                (action,direction) = net.activate(inputs)
                self.do_action(direction,action,fire_grid)
            else:
                random_dir = Direction(random.randint(1,5))
                random_act = Action(random.randint(1,5))
                #self.do_action(random_dir,random_act, fire_grid)
                self.do_action(Direction.NORTH,Action.MOVE,fire_grid)
        if fire_grid[self._current_position.x()][self._current_position.y()].get_state() == CellState.ON_FIRE:
            if self.alive:
                self.alive=False
                fire_grid[self._current_position.x()][self._current_position.y()].remove_one_agent()


