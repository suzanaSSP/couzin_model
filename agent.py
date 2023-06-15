import numpy as np
import random
from typing import List
import math
from math import cos, sin, pi, atan2

# Simulation parameters
S = 1      # velocity
eta = 0.6      # random fluctuation in angle (in radians)
L = 100        # size of box
R = 0.5      # interaction radius
dt = 0.1      # time step
Nt = 200      # number of time steps
plotRealTime = True
k = 0.5        # Attraction factor
a = 1        # agent is visible to other agent in time a


class Agent:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.c = np.array([self.x, self.y])

        self.theta = round(random.uniform(-math.pi, math.pi), 2)
        # self.vx = S * np.cos(self.theta)
        # self.vy = S * np.sin(self.theta)
        self.V = np.array([S * cos(self.theta), S * sin(self.theta)])
        self.W = self.theta

    def move(self):
        # as a reminder this is off the previous self.theta
        # theta_t+1 = theta_t + W * dt
        # x_t+1 = x_t + S*cos(theta_t) * dt
        # the reason this is done with the old theta is that
        # self.x += self.x + S*cos(self.theta) * dt
        # self.y += self.y + S*sin(self.theta) * dt
        # self.V = self.theta + self.W * dt  # this is the new theta
        self.x = self.x + self.V[0] * dt
        self.y = self.y + self.V[1] * dt
        self.V[0] = S * np.cos(self.theta)
        self.V[1] = S * np.sin(self.theta)
        self.theta = self.theta + self.W * dt

    def update_angular_velocity(self, foreigners):
        repulsion_info = np.array([0.0, 0.0])
        sum_of_V = np.array([0.0, 0.0])
        attraction_info = np.array([0.0, 0.0])
        # info2 = np.array([0.0, 0.0])
        # info1 = np.array([0.0, 0.0])
        # attraction_scalar_constant = 1.0
        for agent in foreigners:
            distance = math.dist(self.c, agent.c)

            if 1 > distance:
                # do the repulsion calculation
                repulsion_info = (self.c - agent.c) / \
                    (np.linalg.norm(self.c - agent.c))**2
            elif 8 > distance:
                # do the orientation calculation
                sum_of_V += agent.V
            elif 80 > distance:
                # do the attraction calculation
                attraction_info += (agent.c - self.c)
            else:
                # do nothing
                x = 0

            # elif distance > 3:
            #     # orientation calculation
            #     sum_of_V += np.array([agent.vx, agent.vy])
            # else:
            #     # repulsion calculation
            #     info_repulsion = (self.c - agent.c) / \
            #         (np.linalg.norm(self.c - agent.c))**2
            #     info_dict['info1'] += info_repulsion

            # this will be helpful for the bottom of the repulsion:                 attraction_scalar_constant += np.linalg.norm(
                # agent.c - self.c)

        u3 = attraction_info/np.linalg.norm(attraction_info) if np.linalg.norm(attraction_info) != 0 else np.array([0.0, 0.0])
        u2 = (self.V + sum_of_V)/np.linalg.norm(self.V + sum_of_V) if np.linalg.norm(self.V + sum_of_V) != 0 else np.array([0.0, 0.0])
        u1 = repulsion_info
        U = u1 + u2 + u3
        self.W=k * ((atan2(U[1], U[0])) - self.theta)

        # self.theta = self.theta + w * dt


# class Agent:
#     theta  = random.randint(-1 * int(np.pi), int(np.pi))
#     def __init__(self,x,y) -> None:
#         self.x = x
#         self.y = y
#         self.c = np.array([self.x,self.y])

#         self.vx = S * np.cos(self.theta)
#         self.vy = S * np.sin(self.theta)

#     def move(self):
#         self.x += self.vx * dt
#         self.y += self.vy * dt

#     def update_velocity(self):
#         self.vx = S * np.cos(self.theta)
#         self.vy = S * np.sin(self.theta)

#     def update_angular_velocity(self, foreigners):
#         info_dict = {'info1': np.array([0,0]), 'info2': np.array([0,0]), 'scalar_constant': 1}
#         for agent in foreigners:
#             distance = math.dist(self.c, agent.c)

#             try:
#                 p = min(1, 1/distance)
#             except ZeroDivisionError as e:
#                 p = 1

#             if np.random.default_rng().binomial(1, p, 1) > 0:
#                 info_dict['info1'] += (agent.c - self.c)
#                 info_dict['scalar_constant'] += np.linalg.norm(agent.c - self.c)

#         u3 = info_dict['info1']/info_dict['scalar_constant']
#         w = k * ((np.arctan2(u3[1], u3[0])) - self.theta)

#         self.theta = w
