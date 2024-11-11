import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy

class GameBoard:
    def __init__(self, board_dimensions):
        '''Initialize game board, with no traps or cheeses by default'''
        ### BOARD, STATES
        self.boardDimensions = board_dimensions
        self.statesGraph = nx.grid_2d_graph(board_dimensions[0], board_dimensions[1])
        nx.set_node_attributes(self.statesGraph, False, name='trap')
        nx.set_node_attributes(self.statesGraph, False, name='cheese')
        self.cheeseLocations = np.empty((0,2),dtype=int)
        self.trapLocations = np.empty((0,2),dtype=int)

        ### JERRY DATA
        self.jerryPosition = (board_dimensions[0]-1,board_dimensions[1]-1)
        self.jerryReward = np.zeros(board_dimensions)
        self.jerryQTable = np.zeros(board_dimensions)
        self.jerryActions = { 
            'n': np.array([0,-1], dtype=int),
            'w': np.array([-1,0], dtype=int),
            'e': np.array([1,0], dtype=int),
            's': np.array([0,1], dtype=int),
            'standstill': np.array([0,0], dtype=int)
        }
        self.jerryCurrentPath = []
        self.jerryWon = False

        ### TOM DATA
        self.tomPosition = (0,0) # initialize tom to NW corner
        self.tomReward = np.zeros(board_dimensions)
        self.tomQTable = np.zeros(board_dimensions)
        self.tomActions = {
            'n': np.array([0,-1], dtype=int),
            'w': np.array([-1,0], dtype=int),
            'e': np.array([1,0], dtype=int),
            's': np.array([0,1], dtype=int),
            'standstill': np.array([0,0], dtype=int)
        }
        self.tomCurrentPath = []
        self.tomWon = False

    def InitRandomCheeseAndTraps(self, num_cheeses, num_traps):
        '''Initialize cheese and traps in random locations on the game board'''
        self.cheeseLocations = np.empty((0,2), dtype=int)
        self.trapLocations = np.empty((0,2), dtype=int)

        for _ in range(num_cheeses):
            c = np.random.randint(0, [self.boardDimensions[0], self.boardDimensions[1]])
            # no repeats
            while np.any(np.all(c == self.cheeseLocations, axis=1)):
                c = np.random.randint(0, [self.boardDimensions[0], self.boardDimensions[1]])
            self.cheeseLocations = np.append(self.cheeseLocations, [c], axis=0)

        for _ in range(num_traps):
            t = np.random.randint(0, [self.boardDimensions[0], self.boardDimensions[1]])
            # no repeats, and don't place traps where cheeses have already been placed
            while np.any(np.all(t == self.trapLocations, axis=1)) or np.any(np.all(t == self.cheeseLocations, axis=1)) or list(t) == list(self.jerryPosition):
                t = np.random.randint(0, [self.boardDimensions[0], self.boardDimensions[1]])
            self.trapLocations = np.append(self.trapLocations, [t], axis=0)

        # The following updates the networkx state graph to include cheese and trap information.
        # For now, this is unused, but may be useful later
        for c in self.cheeseLocations:
            self.statesGraph.nodes[tuple(c)]['cheese'] = True
        
        for t in self.trapLocations:
            self.statesGraph.nodes[tuple(t)]['trap'] = True

    def PrintStates(self):
        '''Display state graph'''
        print(self.statesGraph.nodes(data=True))
        nx.draw(self.statesGraph)
        plt.show()
    
    def TomDeterministicUpdate(self):
        '''Move Tom 1 square closer to Jerry'''
        if self.jerryWon:
            return
        self.tomCurrentPath = nx.shortest_path(self.statesGraph, source=self.tomPosition, target=self.jerryPosition)
        if len(self.tomCurrentPath) > 1:
            self.tomPosition = self.tomCurrentPath[1] #path[0] is current position, path[1] is next position in path
        if self.tomPosition == self.jerryPosition:
            self.tomWon = True
        
    def JerryDeterministicUpdate(self):
        '''Move 1 step toward nearest cheese while avoiding tiles with traps or Tom'''
        if self.tomWon:
            return
        
        safe_graph = copy.deepcopy(self.statesGraph)

        # First, remove all nodes where traps exist
        for t in tuple(self.trapLocations):
            safe_graph.remove_node(tuple(t))

        # Next, remove the node where Tom currently is (if it hasn't already been removed)
        if safe_graph.has_node(tuple(self.tomPosition)):
            safe_graph.remove_node(tuple(self.tomPosition))

        # Now, find the nearest cheese to Jerry in the safe graph
        cheese_distances = np.empty((0),dtype=int)
        targetable_cheeses = []
        for c in self.cheeseLocations:
            if safe_graph.has_node(tuple(c)): # this conditional is here so that Tom stepping on a cheese won't break the game
                if nx.has_path(safe_graph,source=self.jerryPosition,target=tuple(c)): # if there is a path to the cheese
                    distance = nx.shortest_path_length(safe_graph, source=self.jerryPosition, target=tuple(c))
                    cheese_distances = np.append(cheese_distances, distance)
                    targetable_cheeses.append(tuple(c))

        # If there exists a reachable cheese:
        if len(targetable_cheeses) > 0:
            target_cheese = tuple(targetable_cheeses[np.argmin(cheese_distances)])

            # Compute a path to the nearest cheese
            self.jerryCurrentPath = nx.shortest_path(safe_graph, source=self.jerryPosition, target=target_cheese)
            self.jerryCurrentPath.append(target_cheese) # add final destination to current path list
            if len(self.jerryCurrentPath) > 1:
                self.jerryPosition = self.jerryCurrentPath[1] #path[0] is current position, path[1] is next position in path

            # check if Jerry has reached a cheese
            if np.any(np.all(self.jerryPosition == self.cheeseLocations, axis=1)):
                self.jerryWon = True
        
        # if no cheeses are targetable, have Jerry do nothing
        else:
            self.jerryCurrentPath = []

def TomStochasticUpdate(self):
    '''TODO: Updates Tom's position using reward function and Q-table'''
    return

def JerryStochasticUpdate(self):
    '''TODO: Updates Jerry's position using reward function and Q-table'''
    return
    