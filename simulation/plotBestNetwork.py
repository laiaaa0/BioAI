import pickle 
from simulation.run_simulation import run 
import os
import neat
from simulation import visualize
from simulation.network import time_const

with open('winner-ctrnn', 'rb') as f:
	c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.ctrnn.CTRNN.create(c, config, time_const)# neat.nn.FeedForwardNetwork.create(c, config)


#visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
#visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

#node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
node_names={}
num_inputs = 26
num_outputs=10
for i in range(1,num_inputs+1):
    node_names[i*-1] = f"input {i}"
for i in range(num_outputs):
    node_names[i] = f"output {i}"


visualize.draw_net(config, c, True, node_names=node_names)

#visualize.draw_net(config, c, view=True, node_names=node_names,
#                   filename="winner-feedforward.gv")
#visualize.draw_net(config, c, view=True, node_names=node_names,
#                      filename="winner-feedforward-enabled.gv", show_disabled=False)
#visualize.draw_net(config, c, view=True, node_names=node_names,
#                     filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)


run(net, 200, 30, True)
