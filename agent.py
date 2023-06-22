import numpy as np
import random
from typing import List
import math


# Simulation parameters
s            = 10      # Constant velocity
Rr           = 300      # Repulsion radius
Ro           = 400      # Orientation radius
dt           = 0.5     # time step
k            = 0.5     # scale for angular velocity calculation
a            = 500      # agent is visible to other agent in time a
L            = 2000    # Size of box
N = 26

# Deal with NaN bugs
np.seterr(divide='ignore', invalid='ignore')

class Agent:
    
    def __init__(self, index, x,y, start_theta) -> None:
        self.index = index
        self.x = x
        self.y = y
        self.c = np.array([self.x,self.y])
        self.theta  = start_theta % (2 * np.pi)
        
        self.vx = s * np.cos(self.theta)
        self.vy = s * np.sin(self.theta)
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])

        
    def get_attractive_agents(self, attractive_agents):
        attraction_info = np.array([0,0], dtype='float64')
        for agent in attractive_agents:
            attraction_info += (agent.c - self.c)
            
        return attraction_info/np.linalg.norm(attraction_info)
                
    def get_repulsion_agents(self, repulsion_agents):
        repulsion_info = np.array([0,0], dtype='float64')
        for agent in repulsion_agents:
            distance = agent.c - self.c
            repulsion_info += distance / (distance @ distance)
            
        return repulsion_info * -1
                
    def get_orientation_agents(self, orientation_agents):
        orientation_info = np.array([0,0], dtype='float64')       
        for agent in orientation_agents:
            orientation_info += agent.v    
            
        norm = np.linalg.norm(orientation_info)    
        return orientation_info / norm if norm > 0 else np.array([np.cos(self.theta + np.pi/2), np.sin(self.theta + np.pi/2)]) 
                
    def find_new_position(self, attractive_agents, repulsion_agents, orientation_agents):
        Ur = self.get_repulsion_agents(repulsion_agents)
        Uo = self.get_orientation_agents(orientation_agents)
        Ua = self.get_attractive_agents(attractive_agents)
        
        u =  Ua 
        w = k * (np.arctan2(u[1], u[0]) - self.theta)
        
        new_position = self.c + (s * self.v * dt)
        new_theta = self.theta + (dt * w)
        new_heading = np.array([np.cos(new_theta), np.sin(new_theta)])

        return {'pos': new_position, 'theta': new_theta, 'heading': new_heading}
    
    def update(self, new_position, new_theta):
        self.c = new_position
        self.theta =  new_theta
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])
"""                
class StubbornAgent(Agent):

    def __init__(self, x=L//2, y=L//2):
        super().__init__(x=L//2, y=L//2)
        
    def move(self):
        self.x = self.x
        self.y = self.y

    def update_angular_velocity(self, foreigners):
        self.theta = self.theta
     

if __name__ == '__main__':
    
    min_pos      = 750      # minimum position of birds
    max_pos      = 1250     # max position of birds
    agent = Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos))
    agents = [Agent(random.randint(min_pos, max_pos), random.randint(min_pos, max_pos)) for i in range(N)]

    for agent in agents:
        agent.update_angular_velocity(agents)

"""
        


   

 