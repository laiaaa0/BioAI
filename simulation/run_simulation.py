import matplotlib.pyplot as plt
from simulation.arena import Arena
a = Arena(num_agents=50)
num_iterations = 60
for i in range(num_iterations):
    a.update()
    a.plot()
plt.show()
