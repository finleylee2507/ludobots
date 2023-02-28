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

    def Evolve(self):

        self.Evaluate(self.parents)
        self.Log_Best()
        # self.Show_Best()
        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)
            self.Log_Best()

    def Evolve_For_One_Generation(self, currentGeneration):

        self.Spawn()  # spawn children
        self.Mutate()  # mutate children
        self.Evaluate(self.children)  # evaluate children fitness by running simulation

        self.Print(currentGeneration)
        self.Select()  # selectively replace parents with children if they have better fitness

    def Print(self, currentGeneration):
        print("\n")
        print(f"---- Generation: {currentGeneration} ---- ")
        for key, parent in self.parents.items():
            print("Parent fitness, ", self.parents[key].fitness, " Children fitness: ", self.children[key].fitness)

        print("-------------------------- ")

        print("\n")

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

            if self.parents[key].fitness < self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        bestValue = self.parents[0].fitness
        bestParent = self.parents[0]
        for key, parent in self.parents.items():
            if parent.fitness > bestValue:
                bestValue = parent.fitness
                bestParent = parent

        print("Best value", bestValue)
        bestParent.Start_Simulation("GUI")

        # self.parent.Evaluate("GUI")

    def Log_Best(self):
        bestValue = self.parents[0].fitness
        for key, parent in self.parents.items():
            if parent.fitness > bestValue:
                bestValue = parent.fitness
        directory = './fitness'

        if not os.path.exists(directory):
            os.mkdir(directory)

        f = open(f"{directory}/{constants.populationSize}_{constants.numberOfGenerations}_{constants.seed}.txt", "a")
        print("Best value: ", bestValue)
        f.write(f"{bestValue}\n")
        f.close()

    def Evaluate(self, solutions):
        for key, solution in solutions.items():
            solution.Start_Simulation("DIRECT")

        for key, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()
