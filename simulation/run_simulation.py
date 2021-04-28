import matplotlib.pyplot as plt
from simulation.arena import Arena
import itertools
import random

# Specifying fire starting locations
init_fire = [(0,0), (20,20), (50,50), (50,51)]

a = Arena(init_fire, num_agents=50, network=None)
# Set up trench
a.add_trench(itertools.product([70], range(30, 70)))
num_iterations = 100
for i in range(num_iterations):
    a.plot()
    a.update()

    # Randomly extinguish at a few (100) places
    extinguish_coords = []
    for i in range(100):
        extinguish_coords.append((random.randint(0,99), random.randint(0,99)))
    a.extinguish(extinguish_coords)

    #print("*** Next iteration ***")
print("Simulation finished")
plt.show()

