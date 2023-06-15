import matplotlib.pyplot as plt
import numpy as np
import math
import random
from agent import Agent
from typing import List

# Simulation parameters
L = 1000        # size of box
dt = 0.1      # time step
Nt = 200      # number of time steps
N = 20    # number of agents
plotRealTime = True

# Simulation Main Loop


def main():

    # Create agents
    # initiating an agent in the bottom left quarter of the window
    # agent = Agent(random.randint(1, (L/2)), random.randint(1, (L/2)))
    agents = [Agent(random.randint(1, (L/2)), random.randint(1, (L/2))) for i in range(N)]
    foreigners = [other_agent for other_agent in agents]  # this basically removes the duplication of the starting agent
    # other_agent for other_agent in agents if other_agent is not agent]  # this basically removes the duplication of the starting agent

    # Prep figure
    fig = plt.figure(figsize=(6, 6), dpi=96)
    ax = plt.gca()

    for i in range(Nt):

        # List of x and y values of agents to put in quiver
        x = [agent.x % L for agent in agents]
        y = [agent.y % L for agent in agents]
        vx = [agent.V[0] for agent in agents]
        vy = [agent.V[1] for agent in agents]

        testx = x[0]
        testy = y[0]
        testvx = vx[0]
        testvy = vy[0]
        # plot all agents
        if plotRealTime or (i == Nt-1):
            plt.cla()
            plt.quiver(x, y, vx, vy, color='r')
            plt.quiver(testx, testy, testvx, testvy, color='b')
            ax.set(xlim=(0, L), ylim=(0, L))
            ax.set_aspect('equal')
            plt.pause(0.001)

        # Update angular velocity
        for agent in agents:
            agent.update_angular_velocity([foreigner for foreigner in agents if foreigner is not agent])

            # move
        for agent in agents:
            agent.move()

    # Save figure
    plt.savefig('activematter.png', dpi=240)
    plt.show()


if __name__ == '__main__':
    main()
