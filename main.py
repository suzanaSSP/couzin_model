import matplotlib.pyplot as plt
import random
from agent import Agent
import math

# Simulation parameters
L            = 50       # size of box
M            = L//4		# smaller box
dt           = 0.001     # time step
Nt           = 5000      # number of time steps
N            = 2       # number of birds
plotRealTime = True


# Simulation Main Loop
def main():
    
    # Create birds
	agent = Agent(random.randint(0,L), random.randint(0,L),)
	agents = [Agent(random.randint(0,L),random.randint(0,L),) for i in range(N)]
	foreigners = [other_agent for other_agent in agents if other_agent is not agent]
   
    # Prep figure
	fig = plt.figure(figsize=(L,L), dpi=96)
	ax = plt.gca()
 
	for i in range(Nt):

		# move
		for agent in agents:
			agent.move()

		# List of x and y values of birds to put in quiver
		x = [agent.x for agent in agents if not math.isnan(agent.x)]
		y = [agent.y for agent in agents if not math.isnan(agent.y)]
		vx = [agent.vx for agent in agents if not math.isnan(agent.vx)]
		vy = [agent.vy for agent in agents if not math.isnan(agent.vy)]

		# Trying to expand the axis according to how the agents
		"""
		mean_of_x_pos = sum(x) / len(x)
		mean_of_y_pos = sum(y) / len(y)
  
		width_min = mean_of_x_pos//2
		width_max = mean_of_x_pos*2
		height_min = mean_of_y_pos//2
		height_max = mean_of_y_pos*2
		"""

		# Make agent come back around if it leaves the axis
		x = [i % L for i in x]
		y = [i % L for i in y]

		# plot in real time
		if plotRealTime or (i == Nt-1):
			# Clearing the axis and plotting again
			plt.cla()
			ax.quiver(x,y,vx,vy,color='r')
			# Limits
			ax.set_xlim(0, L)
			ax.set_ylim(0, L)
			# Pause per frame
			plt.pause(0.0001)
	
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