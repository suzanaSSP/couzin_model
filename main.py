import matplotlib.pyplot as plt
import random
from agent import Agent
import math

# Simulation parameters
min_pos      = 900      # minimum position of birds
max_pos      = 1500       # max position of birds
L            = 2000  	# size of box
Nt           = 5000      # number of time steps
N            = 20      # number of birds
plotRealTime = True


# Simulation Main Loop
def main():
    
    # Create birds
	agent = Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos))
	agents = [Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos)) for i in range(N)]
	foreigners = [other_agent for other_agent in agents if other_agent is not agent]
   
    # Prep figure
	fig = plt.figure(figsize=(6,6), dpi=96)
	ax = plt.gca()
 
	for i in range(Nt):
   
		for agent in agents:
			agent.repel_function()
   
		# List of x and y values of birds to put in quiver
		x = [agent.x for agent in agents]
		y = [agent.y for agent in agents]
		u = [agent.vx for agent in agents]
		v = [agent.vy for agent in agents]
  
		# plot in real time
		if plotRealTime or (i == Nt-1):
			# Clearing the axis and plotting again
			plt.cla()
			ax.quiver(x,y,u,v, color='r')
			ax.set_xlim(0,L)
			ax.set_ylim(0,L)
			# Pause per frame
			plt.pause(0.001)
   
		# Update angular velocity 
		for agent in agents:
			agent.update_angular_velocity(foreigners)

		# move
		for agent in agents:
			agent.move()
		
	# Save figure
	plt.savefig('activematter.png',dpi=240)
	plt.show()
 
if __name__ == '__main__':
	main()