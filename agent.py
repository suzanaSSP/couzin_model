import numpy as np
import random
from typing import List
import math

# TODO: ADJUST TO SCALE

# Simulation parameters
v0           = 5      # velocity
Rr           = 6      # interaction radius
Ro           = 8
dt           = 0.1      # time step
Nt           = 200      # number of time steps
k            = 0.5        # Attraction factor
a            = 1        # agent is visible to other agent in time a
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
        
        for agent in foreigners:   
            distance = math.dist(self.c, agent.c)  
                   
            if 5 > distance > 0:
                info_dict['info1'] += (agent.c - self.c)
                info_dict['scalar_constant'] += np.linalg.norm(agent.c - self.c) 
                
                if np.linalg.norm(self.c - agent.c) <= Ro:
                     info_dict['info2'] += agent.v
                     
                if np.linalg.norm(self.c - agent.c) <= Rr:
                    info_dict['info3'] += np.round(info_dict['info1']/(info_dict['scalar_constant']**2), 3)        
                        
        u1 = -1 * info_dict['info3']
        u2 = (self.v + info_dict['info3'])/np.linalg.norm(self.v + info_dict['info3'])
        u3 = np.round(info_dict['info1']/info_dict['scalar_constant'], 2)
        
        u =  u1 + u2 + u3
        w = k * ((np.arctan2(u[1], u[0])) - self.theta)
        
        self.theta = self.theta + (dt * w)
        

if __name__ == "__main__":
    agent = Agent(random.randint(M, (M+L//2)), random.randint(M, (M+L//2)))
    agents = [Agent(random.randint(M, (M+L//2)), random.randint(M, (M+L//2))) for i in range(20)]
    foreigners = [other_agent for other_agent in agents if other_agent is not agent]
    
    agent.update_angular_velocity(foreigners)
 
    
        


   

 