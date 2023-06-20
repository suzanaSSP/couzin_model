import matplotlib.pyplot as plt
import random
from agent import Agent, StubbornAgent
import math

# Simulation parameters
min_pos      = 500      # minimum position of birds
max_pos      = 1500     # max position of birds
L            = 2000  	# size of box
Nt           = 5000     # number of time steps
N            = 26      	# number of birds
plotRealTime = True


# Simulation Main Loop
def main():
    
    # Create birds
	agent = Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos))
	agents = [Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos)) for i in range(N)]
	foreigners = [other_agent for other_agent in agents if other_agent is not agent]

	# Add stubborn_agent
	stubborn_agent = StubbornAgent()
	agents.append(stubborn_agent)

    # Prep figure
	fig = plt.figure(figsize=(6,6), dpi=96)
	ax = plt.gca()
 
	for i in range(Nt):
   
		# List of x and y values of birds to put in quiver
		x = [agent.x for agent in agents]
		y = [agent.y for agent in agents]
		u = [agent.vx for agent in agents]
		v = [agent.vy for agent in agents]

		# Radius coordinates
		circle_coordinates = [L/2, L/2]
		attraction_circle = plt.Circle((circle_coordinates[0], circle_coordinates[1]), 500, fill=False)
		orientation_circle = plt.Circle((circle_coordinates[0], circle_coordinates[1]), 400, fill=False)
		repulsion_circle = plt.Circle((circle_coordinates[0], circle_coordinates[1]), 300, fill=False)

		# plot in real time
		if plotRealTime or (i == Nt-1):
			# Clearing the axis and plotting again
			plt.cla()
			ax.quiver(x,y,u,v, color='r')
			ax.add_artist(attraction_circle)
			ax.add_artist(orientation_circle)
			ax.add_artist(repulsion_circle)
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