import matplotlib.pyplot as plt
from agent import Agent
import numpy as np
import tqdm
from scipy.stats import bernoulli

# Create a list for each agent with their neighbors. First update everyone's heading, then assign the heading

# Simulation parameters
min_pos      = 750      # minimum position of birds
max_pos      = 1250     # max position of birds
L            = 2000  	# size of box
Nt           = 5000     # number of time steps
N            = 20      	# number of birds


# Formula paramenters
Rr = 1
Ro = 8
a = 80

# Deal with NaN bugs
np.seterr(divide='ignore', invalid='ignore')

class SimulationManager:
    def __init__(self):
        self.visibility_matrix = np.zeros((N, N))
        self.dist_matrix = np.zeros((N, N))
        self.agent_neighbors = {}

        self.agents = []

        self.repulsion_neighbors   = [[] for _ in range(N)]
        self.orientation_neighbors = [[] for _ in range(N)]
        self.attraction_neighbors  = [[] for _ in range(N)]

    def create_agents(self):
        spawn_radius = np.random.uniform(min_pos, max_pos)
        spawn_x_lb = -spawn_radius
        spawn_x_ub = spawn_radius
        spawn_y_lb = -spawn_radius
        spawn_y_ub = spawn_radius
        
        for i in range(N):
            start_x = np.random.uniform(spawn_x_lb, spawn_x_ub)
            start_y = np.random.uniform(spawn_y_lb, spawn_y_ub)
            start_theta = np.random.uniform(-np.pi, np.pi)
    
            new_agent = Agent(i, start_x, start_y, start_theta)
            self.agents.append(new_agent)

            if np.any(np.isnan(new_agent.c)):
                i = 1

        return self.agents

            
    def update_dist(self):
        for i in range(len(self.agents)):
            for j in range(i+1, len(self.agents)):
                distance = np.linalg.norm(self.agents[j].c -  self.agents[i].c)
                
                if np.isnan(distance):
                    i = 1
                self.dist_matrix[i][j] = distance
                self.dist_matrix[j][i] = distance

    def add_agents_to_visibility(self):
        
        self.update_dist()
        for i in range(len(self.agents)):
            for j in range(i + 1, len(self.agents)):
                p_one_agent_sees_other = np.min([1, 1 / self.dist_matrix[i][j]])

                if np.isnan(p_one_agent_sees_other):
                    i = 1

                self.visibility_matrix[i][j] = bernoulli.rvs(p=p_one_agent_sees_other)
                self.visibility_matrix[j][i] = bernoulli.rvs(p=p_one_agent_sees_other)


                # if first neighbor can see the second, append to appropriate lists for the first neighbor depending on their distance
                if self.visibility_matrix[i][j] == 1:
                    self.attraction_neighbors[i].append(self.agents[j])
                    
                    if self.dist_matrix[i][j] < Rr:
                        self.repulsion_neighbors[i].append(self.agents[j])

                    if self.dist_matrix[i][j] < Ro:
                        self.orientation_neighbors[i].append(self.agents[j])

                # if second neighbor can see the first, append to appropriate lists for the second neighbor depending on their distance
                if self.visibility_matrix[j][i] == 1:
                    self.attraction_neighbors[j].append(self.agents[i])
                    
                    if self.dist_matrix[i][j] < Rr:
                        self.repulsion_neighbors[j].append(self.agents[i])

                    if self.dist_matrix[i][j] < Ro:
                        self.orientation_neighbors[j].append(self.agents[i])
            
    def update_agents(self):
        self.add_agents_to_visibility()
        
        agents_to_update = []
        for agent in self.agents:
            a_neighbors = self.attraction_neighbors[agent.index]
            r_neighbors = self.repulsion_neighbors[agent.index]
            o_neighbors = self.orientation_neighbors[agent.index]
            
            agents_to_update.append(agent.find_new_position(a_neighbors, r_neighbors, o_neighbors))
            
        for agent in self.agents:
            agent_updating = agents_to_update[agent.index]
            agent.update(agent_updating['pos'], agent_updating['theta'])
            
        return agents_to_update


    def animate(self, agent_positions):
        fig, ax = plt.subplots()
        for iter in agent_positions:
            agent_xs, agent_ys = np.array([agent['pos'] for agent in iter]).T
            agent_heading_xs, agent_heading_ys = np.array([agent['heading'] for agent in iter]).T / 2

            plt.cla()
            plt.quiver(agent_xs, agent_ys, agent_heading_xs, agent_heading_ys, color='blue')

            avg_x = np.mean(agent_xs)
            avg_y = np.mean(agent_ys)
            ax.set(xlim=(avg_x - L / 2, avg_x + L / 2),
                    ylim=(avg_y - L / 2, avg_y + L / 2))
            ax.set_aspect('equal')
            plt.pause(0.01)

        np.array([agent['pos'] for agent in agent_positions[0]])
    

    def run_simulation(self, num_iters=10):
        self.create_agents()

        all_results = []
        i = 0
        for iter in tqdm.tqdm(range(num_iters), 'Running Simulation...'):
            agent_positions = self.update_agents()

            all_results.append(agent_positions)
            i += 1

            if i > 400:
                j = 1

        return self.animate(all_results)

