#!/usr/bin/env python
# coding: utf-8

# 2021 Modified by: Alejandro Cervantes
# Remember installing pyplot and flask if you want to use WebViewer

from __future__ import print_function

import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import BaseViewer,ConsoleViewer,WebViewer
from scipy.spatial import distance
from scipy.spatial.distance import cityblock

# Calcula la distancia de manhattan
def manhattan(a, b):
    return cityblock(a, b)

# Calcula la distancia euclidea
def euclidea(a, b):
    return distance.euclidean(a, b)


##### Caso base => apartado 5.a #####
# MAP = """
# ########
# #    T #
# # #### #
# #   P# #
# # ##   #
# #      #
# ########
# """

##### Matriz modificada => DFS solucion optima => apartado 5.b ##### 
# MAP = """
# ########
# #T     #
# # #### #
# #    # #
# # ##  P#
# #      #
# ########
# """

##### Matriz modificada => estudio de las diferentes heuristicas
MAP = """
###################################################
#T                                                #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
#                                                P#
###################################################
"""

MAP = [list(x) for x in MAP.split("\n") if x]

COSTS = {
    "up": 1.0,
    # "up": 5.0, # apartado 5.c
    "down": 1.0,
    "right": 1.0,
    "left": 1.0,
}


class GameWalkPuzzle(SearchProblem):

    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "t":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "p":
                    self.goal = (x, y)

        super(GameWalkPuzzle, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in list(COSTS.keys()):
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        # return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
        # return manhattan(state, self.goal)
        return euclidea(state, self.goal)


def searchInfo (problem,result,use_viewer):
    def getTotalCost (problem,result):
        originState = problem.initial_state
        totalCost = 0
        for action,endingState in result.path():
            if action is not None:
                totalCost += problem.cost(originState,action,endingState)
                originState = endingState
        return totalCost

    
    res = "Total length of solution: {0}\n".format(len(result.path()))
    res += "Total cost of solution: {0}\n".format(getTotalCost(problem,result))
        
    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(use_viewer.stats.items())]
        
        for s in stats:
            res+= '{0}: {1}\n'.format(s['name'],s['value'])
    return res


def resultado_experimento(problem,MAP,result,used_viewer):
    path = [x[1] for x in result.path()]

    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print("T", end='')
            elif (x, y) == problem.goal:
                print("P", end='')
            elif (x, y) in path:
                print("·", end='')
            else:
                print(MAP[y][x], end='')
        print()

    info=searchInfo(problem,result,used_viewer)
    print(info)

def main():
    
    # Mostramos tres experimentos
    # problem = GameWalkPuzzle(MAP)
    # used_viewer=WebViewer() 
    # # Probad también ConsoleViewer para depurar
    # # Probad también WebViewer para ver los árboles
    # print("Breadth First Search - Amplitud")
    # result = breadth_first(problem, graph_search=True,viewer=used_viewer)
    # resultado_experimento(problem,MAP,result,used_viewer)
    
    # problem = GameWalkPuzzle(MAP)
    # used_viewer=BaseViewer() 
    # print("Deep First Search - Profundidad")
    # result = depth_first(problem, graph_search=True,viewer=used_viewer)
    # resultado_experimento(problem,MAP,result,used_viewer)

    problem = GameWalkPuzzle(MAP)
    used_viewer=BaseViewer() 
    print("A*")
    result = astar(problem, graph_search=True,viewer=used_viewer)
    resultado_experimento(problem,MAP,result,used_viewer)

if __name__ == "__main__":
    main()
