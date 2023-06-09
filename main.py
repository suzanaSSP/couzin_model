import matplotlib.pyplot as plt
import numpy as np
import math
import random
from agent import Agent
from typing import List

# Simulation parameters
L            = 100        # size of box
R            = 0.5      # interaction radius
dt           = 0.01      # time step
Nt           = 200      # number of time steps
N            = 100      # number of birds
plotRealTime = True

# Simulation Main Loop
def main():
    
    # Create birds
	agent = Agent(random.randint(1,(L/2)), random.randint(1,(L/2)))
	agents = [Agent(random.randint(1,(L/2)), random.randint(1,(L/2))) for i in range(N)]
	foreigners = [other_agent for other_agent in agents if other_agent is not agent]
   
    # Prep figure
	fig = plt.figure(figsize=(6,6), dpi=96)
	ax = plt.gca()
 
	for i in range(Nt):

		# move
		for agent in agents:
			agent.move()

		# List of x and y values of birds to put in quiver
		x = [agent.x for agent in agents]
		y = [agent.y for agent in agents]
		vx = [agent.vx for agent in agents]
		vy = [agent.vy for agent in agents]

		# plot in real time
		if plotRealTime or (i == Nt-1):
			plt.cla()
			plt.quiver(x,y,vx,vy,color='r')
			ax.set(xlim=(0, L), ylim=(0, L))
			ax.set_aspect('equal')	
			plt.pause(0.001)
	
		# update velocities
		for agent in agents:
			agent.update_velocity()
			
		# Update angular velocity 
		for agent in agents:
			agent.update_angular_velocity(foreigners)
   
			
	# Save figure
	plt.savefig('activematter.png',dpi=240)
	plt.show()
 
if __name__ == '__main__':
    main()

