import numpy as np
import random
from typing import List
import math

# TODO: ADJUST TO SCALE

# Simulation parameters
s            = 10      # Constant velocity
Rr           = 300      # Repulsion radius
Ro           = 400      # Orientation radius
dt           = 0.5     # time step
k            = 0.8     # scale for angular velocity calculation
a            = 500      # agent is visible to other agent in time a
L            = 2000    # Size of box


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
        self.v = np.array([np.cos(self.theta), np.sin(self.theta)])

    def move(self):    
        self.x = self.x + (self.vx * dt)
        self.y = self.y + (self.vy * dt)
       
        self.vx = s * np.cos(self.theta)
        self.vy = s * np.sin(self.theta)
        
    def update_angular_velocity(self, foreigners):
        stubborn_agent = StubbornAgent()
        
        repulsion_info = np.array([0.0, 0.0])
        sum_of_V = np.array([0.0, 0.0])
        sum_of_V_squared = np.array([0.0,0.0])
        attraction_info = np.array([0.0, 0.0])

        # Adding up all the distances and velocities of each agent, needed for calculating the next equations           
        distance = math.dist(self.c, stubborn_agent.c)  

        # Seeing if there are visible agents       
        if a < distance:
            attraction_info += (stubborn_agent.c - self.c)            
    
            # Radius of orientation
            if np.linalg.norm(stubborn_agent.c - self.c) <= Ro:
                sum_of_V += stubborn_agent.v
                sum_of_V_squared  += (stubborn_agent.v **2)
            
            # Radius of repulsion    
            if np.linalg.norm(stubborn_agent.c - self.c) <= Rr:
                repulsion_info += (stubborn_agent.c - self.c)/(np.linalg.norm(stubborn_agent.c - self.c)**2)
                  
        repulsion_equation = repulsion_info
        orientation_equation = (self.v + sum_of_V)/np.linalg.norm(self.v + sum_of_V_squared)
        attraction_equation = attraction_info/np.linalg.norm(attraction_info)
        
        u = attraction_equation
        
        w = k * ((((math.atan2(u[1], u[0]) - self.theta) + math.pi) % (2*math.pi))- math.pi)
        
        self.theta = self.theta + (dt * w)
        
class StubbornAgent(Agent):

    def __init__(self, x=L//2, y=L//2):
        super().__init__(x=L//2, y=L//2)
        
    def move(self):
        self.x = self.x
        self.y = self.y

    def update_angular_velocity(self, foreigners):
        self.theta = self.theta
     




        


 
    
        


   

 