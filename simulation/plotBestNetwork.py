import pickle 
from simulation.run_simulation import run 

with open('winner-feedforward', 'rb') as f:
	bestNet = pickle.load(f)


run(bestNet, 100, 50, True)
