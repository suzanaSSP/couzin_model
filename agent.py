import numpy as np
import random
from typing import List
import math
np.seterr(divide='ignore', invalid='ignore')


# TODO: ADJUST TO SCALE

# Simulation parameters
v0           = 5      # velocity
Rr           = 6      # interaction radius
Ro           = 8
dt           = 0.1      # time step
Nt           = 200      # number of time steps
k            = 0.5        # Attraction factor
a            = 80        # agent is visible to other agent in time a
dt           = 0.001     # time step
L            = 50       # range of x, y values
M            = L//4		# smaller box


class Agent:
    theta  = random.randint(-1 * int(np.pi), int(np.pi))
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.c = np.array([self.x,self.y])
        
        self.vx = v0 * np.cos(self.theta)
        self.vy = v0 * np.sin(self.theta)
        self.v = np.array([self.vx, self.vy])

    def move(self):    
        self.x += self.vx * dt
        self.y += self.vy * dt
       
    def update_velocity(self):
        self.vx = self.vx + (v0 * np.cos(self.theta))
        self.vy = self.vy + (v0 * np.sin(self.theta))
        
    def update_angular_velocity(self, foreigners):
        info_dict = {'info1': np.array([0,0], dtype=np.float64), 
                     'info2': np.array([0,0], dtype=np.float64), 
                     'info3': np.array([0,0], dtype=np.float64), 
                     'scalar_constant': 0, 
                     }
        
        # Adding up all the distances and velocities of each agent, needed for calculating the next equations
        for agent in foreigners:  
             
            distance = math.dist(self.c, agent.c)  
            
            # Seeing if there are visible agents       
            if a > distance > 0:
                info_dict['info1'] += (agent.c - self.c)
                info_dict['scalar_constant'] += np.linalg.norm(agent.c - self.c) 
                """ 
                    # Radius of orientation
                    if np.linalg.norm(self.c - agent.c) <= Ro:
                        info_dict['info2'] += agent.v
                    
                    # Radius of repulsion    
                    if np.linalg.norm(self.c - agent.c) <= Rr:
                        info_dict['info3'] += np.round(info_dict['info1']/(info_dict['scalar_constant']**2), 3) 
                    """
                   
        #u1 = -1 * info_dict['info3']
        #u2 = (self.v + info_dict['info3'])/np.linalg.norm(self.v + info_dict['info3'])
        u3 = info_dict['info1']/info_dict['scalar_constant']
        
        u =  u3
        w = k * (np.arctan2(u[1], u[0]) - self.theta)
        
        self.theta = self.theta + (dt * w)
        


 
    
        


   

 