import numpy as np
import random
from typing import List
import math

# TODO: ADJUST TO SCALE

# Simulation parameters
v0           = 5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 10        # size of box
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
k            = 0.5        # Attraction factor
a            = 80        # agent is visible to other agent in time a
dt           = 0.1     # time step
L            = 2000       # range of x, y values
M            = L//4		# smaller box

# Deal with NaN bugs
np.seterr(divide='ignore', invalid='ignore')

class Agent:
    
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.c = np.array([self.x,self.y])
        self.theta  = round(random.uniform(-math.pi, math.pi), 2)
        
        self.vx = s * np.cos(self.theta)
        self.vy = s * np.sin(self.theta)
        self.v = np.array([self.vx, self.vy])

    def move(self):    
        self.x = self.x + (self.vx * dt)
        self.y = self.y + (self.vy * dt)
       
        self.vx = s * np.cos(self.theta)
        self.vy = s * np.sin(self.theta)
        
    def update_angular_velocity(self, foreigners):
        
        # Repel axis units
        xlim = [0, L]
        ylim = [0,L]
        
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
        
                # Radius of orientation
                if np.linalg.norm(self.c - agent.c) <= Ro:
                    info_dict['info2'] += agent.v
                
                # Radius of repulsion    
                if np.linalg.norm(self.c - agent.c) <= Rr:
                    info_dict['info3'] += info_dict['info1']/(info_dict['scalar_constant']**2)
                  
        repulsion_equation = -1 * info_dict['info3']
        orientation_equation = (self.v + info_dict['info3'])/np.linalg.norm(self.v + info_dict['info3'])
        attraction_equation = info_dict['info1']/info_dict['scalar_constant']
        
        u =  attraction_equation
        
        w = k * ((((math.atan2(u[1], u[0]) - self.theta) + math.pi) % (2*math.pi)) - math.pi)
        
        self.theta = self.theta + (dt * w)
        
    def repel_function(self):
        xlim = [0,L]
        ylim = [0,L]
        error_line = 50
        
        
        if self.x < xlim[0] + error_line:
            self.x += error_line
            self.theta = self.theta * -1
        elif self.x > xlim[1] - error_line:
            self.x -= error_line
            self.theta = self.theta*-1
        if self.y < ylim[0] + error_line:
            self.y += error_line
            self.theta = self.theta*-1
        elif self.y > ylim[1] - error_line:
            self.y += error_line
            self.theta = self.theta*-1
     




        


 
    
        


   

 