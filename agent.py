import numpy as np
import random
from typing import List
import math

# Simulation parameters
v0           = 5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 10        # size of box
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 20      # number of birds
plotRealTime = True
k            = 0.5        # Attraction factor
a            = 1        # agent is visible to other agent in time a

class Agent:
    theta  = random.randint(-1 * int(np.pi), int(np.pi))
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.c = np.array([self.x,self.y])
        
        self.vx = v0 * np.cos(self.theta)
        self.vy = v0 * np.sin(self.theta)

    def move(self):    
        self.x += self.vx * dt
        self.y += self.vy * dt
       
    def update_velocity(self):
        self.vx = v0 * np.cos(self.theta)
        self.vy = v0 * np.sin(self.theta)
        
    def update_angular_velocity(self, foreigners):
        info_dict = {'info1': np.array([0,0]), 'info2': np.array([0,0]), 'scalar_constant': 1}
        for agent in foreigners:
            distance = math.dist(self.c, agent.c)
            
            try:
                p = min(1, 1/distance)
            except ZeroDivisionError as e:
                p = 1
                
            if np.random.default_rng().binomial(1, p, 1) > 0:
                info_dict['info1'] += (agent.c - self.c)
                info_dict['scalar_constant'] += np.linalg.norm(agent.c - self.c)
                
        u3 = info_dict['info1']/info_dict['scalar_constant']
        w = k * ((np.arctan2(u3[1], u3[0])) - self.theta)
        
        self.theta = w
        


   

 