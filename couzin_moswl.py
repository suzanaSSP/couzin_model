import matplotlib.pyplot as plt
import numpy as np
import math
import random

# Simulation parameters
v0           = 0.5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 5        # size of box
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 2        # number of birds
plotRealTime = True
k            = 2        # Attraction factor
a            = 1        # agent is visible to other agent in time a

# Initialize
np.random.seed(30)      # set the random number generator seed

# bird positions
x = np.random.rand(N,1)*L
y = np.random.rand(N,1)*L
x_list = [random.randint(1, L) for i in range(N)]
y_list = [random.randint(1, L) for i in range(N)]
# Turning x which is an array into a list, so I can create c which is the position of the agent. It'll be easier to do the equations  

# bird velocities
theta = 2 * np.pi * np.random.rand(N,1)
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

# Prep figure
fig = plt.figure(figsize=(6,6), dpi=96)
ax = plt.gca()

# Simulation Main Loop
for i in range(Nt):

	# move
	x_list = [i + vx*dt for i in x_list]
	y_list = [i + vy*dt for i in y_list]
 
	# update velocities
	vx = v0 * np.cos(theta)
	vy = v0 * np.sin(theta)
		
	# find mean angle of neighbors within R

	info_dict = {'info1': np.array([0.0,0.0]), 'info2': np.array([0.0,0.0])}
	for i in range(1, N):
		# Turning x which is an array into a list, so I can create c which is the position of the agent. It'll be easier to do the equations  	
		c_j = np.array([x_list[i], y_list[i]])
		c_i = np.array([x_list[0], y_list[0]])

		# I can see you
		distance = math.dist(c_i, c_j)
		p = min(1, 1/distance)
		if np.random.default_rng().binomial(1, p, 1) > 0:
			info_dict['info1'] += (c_j - c_i)
			info_dict['info2'] += (c_j**2 - c_i**2)
		
	# Formula 7
	u3 = info_dict['info1'] / info_dict['info2']
	w = k * (math.atan2(u3[0], u3[1]) - theta)
	theta = w
	
	# plot in real time
	if plotRealTime or (i == Nt-1):
		plt.cla()
		plt.quiver(x,y,vx,vy,color='r')
		ax.set(xlim=(0, L), ylim=(0, L))
		ax.set_aspect('equal')	
		plt.pause(0.001)
			
# Save figure
plt.savefig('activematter.png',dpi=240)
plt.show()

