from simulation.geometry import Rectangle, Point
from simulation.firefighter import Firefighter
from simulation.cell import Cell, CellState

import unittest
import math


class TestFighter(unittest.TestCase):
    def test_init(self):
        rect = Rectangle(-10, -10, 20, 20)
        point = Point(8, 4)
        a = Firefighter(rect, 0.3, point, 0)
        self.assertEqual(point, a.position())

    def test_network_input(self):
        rect = Rectangle(0, 0, 10, 10)
        point = Point(5, 5)
        terrain_map = [[Cell((j,i)) for i in range(10)] for j in range(10)]
        expected_input_list = [1] * 18 + [ 1, 0, 1, 0, 1, 0,1,0]
        


        for i in range(4, 7):
            for j in range(4, 7):
                terrain_map[i][j].set_state(CellState.BURNABLE)
                terrain_map[i][j].add_one_agent()

        f = Firefighter(rect, 0.3, point, 0)
        result_input = f.get_network_input(terrain_map)
        self.assertEqual(result_input, expected_input_list)

        f._current_position = Point(0, 0)

        for i in range(2):
            for j in range(2):
                terrain_map[i][j].set_state(CellState.ON_FIRE)
                terrain_map[i][j].add_one_agent()
        expected_list_corner = [0,0, 2,1, 2,1, 0,0, 2,1, 2,1, 0,0, 0,0, 0,0,0,0,1,0,1,0,0,0]
        self.assertEqual(
            f.get_network_input(terrain_map),
            expected_list_corner)
