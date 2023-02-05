import copy
import os
import sys

import constants
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(constants.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Print(self):
        for key, parent in self.parents.items():
            print("Parent fitness, ", self.parents[key].fitness, " Children fitness: ", self.children[key].fitness)

        print(" ")

    def Evolve(self):

        self.Evaluate(self.parents)

        for currentGeneration in range(constants.numberOfGenerations):
            print("Generation: ",currentGeneration)
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)

        #
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for key, parent in self.parents.items():
            self.children[key] = copy.deepcopy(parent)
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key, child in self.children.items():
            child.Mutate()

    def Select(self):
        for key, parent in self.parents.items():

            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        bestValue=sys.maxsize
        bestParent=None
        for key,parent in self.parents.items():
            if parent.fitness<bestValue:
                bestValue=parent.fitness
                bestParent=parent

        print("Best value",bestValue)
        bestParent.Start_Simulation("GUI")

        # self.parent.Evaluate("GUI")
        pass

    def Evaluate(self, solutions):
        for key, solution in solutions.items():
            solution.Start_Simulation("DIRECT")

        for key, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()
