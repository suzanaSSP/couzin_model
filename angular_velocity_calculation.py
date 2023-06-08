import numpy as np
import math

# Simulation parameters
v0           = 0.5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 10      # size of box
R            = 1      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 100        # number of birds
plotRealTime = True

# bird positions
x = np.random.rand(N,1)*L
y = np.random.rand(N,1)*L

# bird velocities
theta = 2 * np.pi * np.random.rand(N,1)
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

# Information needed to calculate angular velocity. Sum of velocities, sum of scalar constant, etc.
info_dict = {'scalar_constant': 0, 'info1': np.empty((2,2)), 'info2': np.empty((2,2)), 'info3': np.empty((2,2)), 'info4': np.empty((2,2))}
for i in range(1, N):
    # Turning x which is an array into a list, so I can create c which is the position of the agent. It'll be easier to do the equations    
    x_list = np.concatenate(x).tolist()
    y_list = np.concatenate(y).tolist()
    c_j = np.array([x[i], y[i]])
    c_i = np.array([x[0], y[0]])
    
    info_dict['scalar_constant'] += math.dist(c_j, c_i)
    
    # Sum needed for formula 5 and 7
    info_dict['info1'] += (1/np.linalg.norm(info_dict['scalar_constant'])) * (c_j - c_i)
    # Sum needed for formula 6
    info_dict['info2'] += np.array([np.cos(theta), np.sin(theta)])
    info_dict['info3'] += np.array([np.cos(theta)**2, np.sin(theta)**2])
    # Sum needed for formula 7
    info_dict['info4'] += c_j - c_i

print(info_dict)

u1 = -1 * info_dict['info1']
u3 = info_dict['info4']/info_dict['info1']



