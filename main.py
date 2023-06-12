import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from agent import Agent
import statistics

# Simulation parameters
L            = 50       # size of box
M            = L//4		# smaller box
dt           = 0.001     # time step
Nt           = 5000      # number of time steps
N            = 100        # number of birds
plotRealTime = True

# Simulation Main Loop
def main():
    
    # Create birds
	agent = Agent(random.randint(0,L), random.randint(0,L),)
	agents = [Agent(random.randint(0,L),random.randint(0,L),) for i in range(20)]
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
  
		# apply periodic BCs
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

