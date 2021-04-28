import matplotlib.pyplot as plt
from simulation.arena import Arena

# Specifying fire starting locations
init_fire = [(0,0), (20,20), (50,50), (50,51)]

a = Arena(init_fire, num_agents=50)
num_iterations = 60
for i in range(num_iterations):
    a.update()
    a.plot()
    print("*** Next iteration ***")
print("Simulation finished")
plt.show()