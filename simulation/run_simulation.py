import matplotlib.pyplot as plt
from simulation.arena import Arena
a = Arena(num_agents=10)
num_iterations = 100
for i in range(num_iterations):
    a.update()
    a.plot()
plt.show()
