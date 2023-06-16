import numpy as np
import random
from typing import List
import math

# Simulation parameters
v0           = 5      # velocity
L            = 10        # size of box
Rr            = 1     # interaction radius
Ro            = 8
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
        self.v = np.array([self.vx, self.vy])
                          
    def move(self):    
        self.x += self.vx * dt
        self.y += self.vy * dt
       
    def update_velocity(self):
        self.vx = v0 * np.cos(self.theta)
        self.vy = v0 * np.sin(self.theta)
        self.v = np.array([self.vx, self.vy])
        
    def update_angular_velocity(self, foreigners):
        info_dict = {
            'info1': np.array([0, 0], dtype=np.float64),
            'info2': np.array([0, 0], dtype=np.float64),
            'scalar_constant': 1,
            'info3': np.array([0, 0], dtype=np.float64),
            'info4': np.array([0, 0], dtype=np.float64)
        }

        for other_agent in foreigners:
            distance = math.dist(self.c, other_agent.c)
            
            try:
                p = min(1, 1/distance)
            except ZeroDivisionError as e:
                p = 1
                
            # For formula 7
            if np.random.default_rng().binomial(1, p, 1) > 0:
                info_dict['info1'] += (other_agent.c - self.c)
                info_dict['scalar_constant'] += np.linalg.norm(other_agent.c - self.c)

                """
                Umask = np.array([False, False])  # Example Umask array
                # For formula 5
                if np.linalg.norm(self.c - other_agent.c) <= Rr:       
                    # Check if the slice is empty before computing the mean
                    if np.any(~Umask):
                        info_dict['info3'] += (other_agent.c - self.c)/(np.linalg.norm(other_agent.c - self.c)**2)
                    else:
                        amean = 0  # Set a default value or handle the case when the slice is empty


                   
                
                # For formula 6
                if np.linalg.norm(self.c - other_agent.c) <= Ro:   
                    info_dict['info4'] +=  other_agent.v
                

        u1 = -1 * info_dict['info3']
        u2 = (self.v + info_dict['info4'])/np.linalg.norm(self.v + info_dict['info4'])
        """
        u3 = info_dict['info1']/info_dict['scalar_constant']
        w = k * ((np.arctan2(u3[1], u3[0])) - self.theta)
        
        self.theta = w
        


   

 