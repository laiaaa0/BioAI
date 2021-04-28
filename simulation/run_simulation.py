import matplotlib.pyplot as plt
from simulation.arena import Arena
import itertools
import random

def run(network=None, show_plot=True):
    # Specifying fire starting locations
    init_fire = [(0,0), (20,20), (50,50), (50,51)]

    a = Arena(init_fire, num_agents=100)
    # Set up trench
    a.add_trench(itertools.product([70], range(30, 70)))
    num_iterations = 50
    for i in range(num_iterations):
        if show_plot:
            a.plot()
        a.update()

        # Randomly extinguish at a few (100) places
        extinguish_coords = []
        for i in range(100):
            extinguish_coords.append((random.randint(0,99), random.randint(0,99)))
        a.extinguish(extinguish_coords)

    if show_plot:
        print("Simulation finished")
        plt.show()
    return a.get_fitness_function()

if __name__=="__main__":
    print(run(None,True))