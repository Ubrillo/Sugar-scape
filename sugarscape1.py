from enum import Enum 
import math
import random

#directional cardinal vectors
class Direction(Enum):
    NORTH = -1, 0 
    SOUTH = 1, 0
    EAST = 0, 1
    WEST = 0,-1

#defines the agent class
class Agent:
    def __init__(self,name):
        self.energy = 10 #energy of the agent
        self.sight = 3 #stores agent's sight range
        self.name = name #holds the name of an agent
        self.pos = None #holds current position of an agent
        self.vision = {} #holds all states visible in agent sight
        self.detail = "" #holds text description about agent
    
    #moves agent from a state to another
    def move(self):
        loc = self.whereTo() # determines the next location for agent
        if loc: #checks if intended location is valid
            world.grid[self.pos[0]][self.pos[1]] = None
            world.grid[loc[0]][loc[1]] = self
            self.updateEnergy(loc)
            self.vision = {}
            self.pos = loc
  
    #update agent's energy level and reduce sugar level in the world
    def updateEnergy(self, loc):
        if loc in world.sugar:
            self.energy += world.sugar[loc] #increase the energy level of an agent
            world.reduceSugar(loc) #reduce sugar level in world to zero
        
        self.detail += f"Agent's Energy: {self.energy}\n" 
        self.detail += f'sugar Level: {world.sugar[loc]}\n'

    #determines agent's next state
    #return state with highest sugar level that is free
    #return agent current state if no new state is found
    def whereTo(self):
        self.computeVision()
        vision_sugar = {}
        
        for key in self.vision:
            if key in world.sugar and (self.isFree(key) or key == self.pos):
                vision_sugar[key] = world.sugar[key]  
        try:
            max_vision = max(vision_sugar, key=vision_sugar.get)
            max_visions = [key for key, value in vision_sugar.items() if value == vision_sugar[max_vision]]
            rand = random.randint(0, len(max_visions)-1)
            max_vision = max_visions[rand]

            self.detail += f'vision_sugar: {vision_sugar} - length: {len(vision_sugar)}\n'
            self.detail += f'next move: {max_vision}\n'
            return max_vision
        except ValueError:
            return self.pos
    
    #Checks of a specified state is free 
    #@para: loc - state to be checked
    #return True is free, False otherwise
    def isFree(self, loc):
        if world.grid[loc[0]][loc[1]] == None:
            return True
        return False

    #compute vision search for states in the world
    def computeVision(self):
        whereTo = self.pos
        self.vision = {}
        self.vision[whereTo] = world.grid[whereTo[0]][whereTo[1]]
        
        for direction in Direction:
            for i in range (self.sight):
                whereTo = tuple((x + y)%20 for x, y in zip(whereTo, direction.value))
                self.vision[whereTo] = world.grid[whereTo[0]][whereTo[1]]
            whereTo = self.pos

        self.detail += f'vision range: {self.vision} - length: {len(self.vision)}\n'
          
    #reduces agent energy by 1
    def metabolism(self):
        self.energy  -= 1
        #agent dies
        if self.energy <= 0:
            world.grid[self.pos[0]][self.pos[1]] = None
            world.agents.remove(self)
    
    #show detail of an agent
    def show_details(self):
        self.detail = ""
        self.detail += f'agent: {self.name}\n'
        self.detail += f'current position: {self.pos}\n'
        #self.computeVision()
        self.whereTo()
        
        print(self.detail)

#creating agents objects
agents = []
for i in range(20):
     agent = Agent('Agent'+str(i+1))
     agents.append(agent)

#defines gridworld
class GridWorld:
    def __init__(self):
        self.capacity = {}
        self.sugar = {}
        self.grid = None
        self.size = 20,20 #A 20X20 grid world
        self.detail = ""
        self.createWorld()
        self.placeAgent(agents)
        self.agents = agents
        
    #Create the world
    def createWorld(self):
        self.grid = []
        for row in range(self.size[0]):
            self.grid.append([])
            for col in range(self.size[1]):
                self.grid[row].append(None)
                self.capacity[(row, col)] = row+col
                self.sugar[(row, col)] = row+col
                        
        self.detail += f'sugar: {self.sugar}\n'
        self.detail += f'capacity: {self.capacity}\n'

    #put agents in the world randomly
    def placeAgent(self, agents):
        for agent in agents:
            rand = random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)
            while self.grid[rand[0]][rand[1]] != None:
                rand = random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)
            self.grid[rand[0]][rand[1]] = agent
            agent.x, agent.y = rand[0], rand[1]
            agent.pos = agent.x, agent.y
    
    def reduceSugar(self, loc):
        self.sugar[loc] = 0

    
    #display the world
    def show_world(self):
        print()
        for row in self.grid:
            for obj in  row:
                print('[', end='')
                if obj == None:
                    print('  ', end='')
                else: #type(obj) == type(Agent):
                    if len(obj.name[5:]) == 1:
                        print(str(0)+obj.name[5:], end='')
                    if len(obj.name[5:]) == 2:
                        print(obj.name[5:], end='')
                print(']', end=' ')
            print()
    #return the size of the world
    def getSize(self):
        return self.size
print("Initial world")
world = GridWorld()#create a new world
# world.show_world() # display the new world upon creation

#Surgar Growth Phase
def sugarGrowth():
    for key in world.sugar:
        world.sugar[key]  += 1
        if world.sugar[key] > world.capacity[key]:
            world.sugar[key] = world.capacity[key]

#Movement Phase
def movement():
    random.shuffle(world.agents) #shuffles the list of agent randomly
    for agent in world.agents:
        agent.move()

#Consumption Phase
def metabolism():
    for agent in world.agents:
        agent.metabolism()


########################### SIMULATION FOR SIMPLE SUGASCAPE ###############################
import csv
import random
import matplotlib.pyplot as plt
gents = world.agents
sum_energy = []
turn = []
turn_150500 = []
pos = []
sugar_level = []


for i in range(1, 501):
    sugarGrowth()
    movement()
    metabolism()
    
    turn.append(i)
    total = 0
    for agent in world.agents:
        total += agent.energy
    sum_energy.append(total)

    if i == 1:
        for agent in world.agents:
            pos.append(agent.pos)
        for sugar in world.sugar:
            sugar_level.append(world.sugar[sugar])

    elif i == 50:
        for agent in world.agents:
            pos.append(agent.pos)
        for sugar in world.sugar:
            sugar_level.append(world.sugar[sugar])
    elif i == 500:
        for agent in world.agents:
            pos.append(agent.pos)
        for sugar in world.sugar:
            sugar_level.append(world.sugar[sugar])

#DATA COLLECTION

#writing energy data into file
write_file = open('energy.csv', 'w', newline='')
csv_writer = csv.writer(write_file)
for i in range (len(turn)):
    csv_writer.writerow([turn[i], sum_energy[i]])
write_file.close()

#writing agents' posiitions data into file
write_file = open('positions.csv', 'w', newline='')
csv_writer = csv.writer(write_file)
for pos in pos:
    csv_writer.writerow([pos[0], pos[1]])
write_file.close()

#writing sugar level data into file
write_file = open('sugar.csv', 'w', newline='')
csv_writer = csv.writer(write_file)
for level in sugar_level:
    csv_writer.writerow([level])
write_file.close()

#plot sugarscape and agent position
def plotScape(agents, sugar_list, turn):
    # Parameters for Sugarscape
    import numpy as np
    grid_size = 20  # 20x20 grid

    sugar = []
    for row in range (grid_size):
        sugar.append([])
        for col in range (grid_size):
            sugar[row].append(sugar_list[col])
    # Initialize agents with random positions
    agents = [{'x': pos[0], 'y': pos[1]} for pos in agents]

    # Function to visualize Sugarscape with agents
    def visualize_sugarscape(sugar, agents):
        plt.figure(figsize=(8, 8))
        
        # Plot the heatmap with green colormap
        plt.imshow(sugar, cmap='Greens', origin='upper')
        
        # Overlay agent positions
        for agent in agents:
            plt.scatter(agent['y'], agent['x'], color='blue', s=70, label='Agent' if agent == agents[0] else "")
        
        plt.title("Agents Position and Sugar Level in Turn "+str(turn))
        # plt.colorbar(label="Sugar Levels")
        plt.legend(loc='upper right')
        plt.gca().axes.xaxis.set_visible(False)  # Hide the x-axis
        plt.gca().axes.yaxis.set_visible(False)  # Hide the y-axis
 
        plt.show()
     
    # Visualize the Sugarscape and agents
    visualize_sugarscape(sugar, agents)

#plot the energy vs turn
def plotEnergy():
    read_file = open('energy.csv')
    csv_reader = csv.reader(read_file)
    read_list1 = []
    read_list2 = []
    for row in csv_reader:
        # print(row)
        read_list1.append(int(row[0]))
        read_list2.append(int(row[1]))
    read_file.close()

    plt.figure(figsize=(10, 4))
    plt.plot(read_list1, read_list2, linestyle='--')
    plt.xlabel('Turns')
    plt.ylabel('Energy')
    plt.title("Total Agents' Energy per Turn")
    
#read from file and call sugarscape functioin for plotting
def plot2():
    read_file = open('positions.csv')
    csv_reader = csv.reader(read_file)
    pos_list = []
    sugar_level = []

    for row in csv_reader:
        pos_list.append((int(row[0]), int(row[1])))
    read_file.close()

    read_file = open('sugar.csv')
    csv_reader = csv.reader(read_file)
    for row in csv_reader:
        sugar_level.append(int(row[0]))
    read_file.close()

    plotScape(pos_list[:20], sugar_level[:400], 1)
    plotScape(pos_list[20:40], sugar_level[400:800], 50)
    plotScape(pos_list[40:], sugar_level[800:], 500)
    
plotEnergy()
plot2()
