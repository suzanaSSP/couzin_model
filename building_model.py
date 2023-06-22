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
plotRealTime = True

# Agent parameters
agents            = []
dist_matrix       = np.zeros((N, N))
visibility_matrix = np.zeros((N, N))

# Formula paramenters
Rr = 1
Ro = 8
a = 80

# Visilibilty parameters
repulsion_neighbors   = [[] for i in range(len(agents))]
orientation_neighbors = [[] for i in range(len(agents))]
attractive_neighbors  = [[] for i in range(len(agents))]

def create_agents():
	spawn_radius = np.random.uniform(min_pos, max_pos)
	spawn_x_lb = - spawn_radius
	spawn_x_ub = spawn_radius
	spawn_y_lb = - spawn_radius
	spawn_y_ub = spawn_radius

	for i in range(N):
		start_x = np.random.uniform(spawn_x_lb, spawn_x_ub)
		start_y = np.random.uniform(spawn_y_lb, spawn_y_ub)
		start_theta = np.random.uniform(-np.pi, np.pi)
  
		new_agent = Agent(i, start_x, start_y, start_theta)

		agents.append(new_agent)
  
	return agents

def update_dist():
    for i in range(len(agents)):
        for j in range(len(agents)):
            distance = np.linalg.norm(agents[j].c -  agents[i].c)
            
            dist_matrix[i][j] = distance
            dist_matrix[j][i] = distance

def update_visibilities():
    
    update_dist()
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            p = np.min([1, 1/dist_matrix[i][j]])

            visibility_matrix[i][j] = bernoulli.rvs(p=p)
            visibility_matrix[j][i] = bernoulli.rvs(p=p)

            # if first neighbor can see the second, append to appropriate lists for the first neighbor depending on their distance
            if visibility_matrix[i][j] == 1:
                attractive_neighbors[i].append(agents[j])
                
                if dist_matrix[i][j] < Rr:
                    repulsion_neighbors[i].append(agents[j])

                if dist_matrix[i][j] < Ro:
                    orientation_neighbors[i].append(agents[j])

            # if second neighbor can see the first, append to appropriate lists for the second neighbor depending on their distance
            if visibility_matrix[j][i] == 1:
                attractive_neighbors[j].append(agents[i])
                
                if dist_matrix[i][j] < Rr:
                    repulsion_neighbors[j].append(agents[i])

                if dist_matrix[i][j] < Ro:
                    orientation_neighbors[j].append(agents[i])
        
def update_agents():
    update_visibilities()
    
    agents_to_update = []
    for agent in agents:
        attractive_neighbors = attractive_neighbors[agent.index]
        repulsion_neighbors = repulsion_neighbors[agent.index]
        orientation_neighbors = orientation_neighbors[agent.index]
        
        agents_to_update.append(agent.find_new_position(attractive_neighbors, repulsion_neighbors, orientation_neighbors))
        
    for agent in agents:
        agent_updating = agent_updating[agent.index]
        agent.update(agent_updating['pos'], agent_updating['theta'])
        
    return agents_to_update


def animate(agent_positions):
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
 

def run_simulation(num_iters=10):
	create_agents()

	all_results = []
	i = 0
	for iter in tqdm.tqdm(range(num_iters), 'Running Simulation...'):
		agent_positions = update_agents()

		all_results.append(agent_positions)
		i += 1

		if i > 400:
			j = 1

	return animate(all_results)

if __name__ == '__main__':
    update_visibilities()
