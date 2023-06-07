
import matplotlib.pyplot as plt
import numpy as np
from agent import Agent
from typing import List
import math

# Simulation parameters
v0           = 0.5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 5        # size of box
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 300      # number of birds
plotRealTime = True
R            = 1		# Radius of repulsion
w            = 0.5		# Angular velocity
k            = 2

# bird positions
x = np.random.rand(N,1)*L
y = np.random.rand(N,1)*L 
agent = Agent(x,y)

# Initialize
np.random.seed(30)      # set the random number generator seed

birds = [Agent(x,y) for i in range(N)]

neighbors: List[Agent] = list(filter(lambda other_agent: other_agent != agent, birds))

agents_in_radius = []
for other_agent in neighbors:
    distance = np.linalg.norm(other_agent.c, agent.c)
    p = min(1, 1/distance)
    if np.random.default_rng().binomial(1, p, 1) > 0:
        agents_in_radius.append(other_agent)

for other_agent in agents_in_radius:
	u1 = sum((other_agent.c - agent.c)/(np.linalg.norm(other_agent.c - agent.c))**2)
	u2 = (v0 + v0*len(agents_in_radius))/v0**2 + (v0*len(agents_in_radius)**2)
	u3 = sum(other_agent.c - agent.c)/ sum((other_agent.c - agent.c)**2)
 
u = u1 + u2 + u3



#np.linalg.norm()
print(u)