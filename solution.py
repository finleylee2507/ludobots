import os
import random
import time

import numpy as np

import constants as c
from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.myID = nextAvailableID

    def Evaluate(self, directOrGUI):
        pass

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Brain()
        self.Create_Body()
        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"./fitness{str(self.myID)}.txt"):
            time.sleep(0.01)

        fitnessFile = open(f"./fitness{str(self.myID)}.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system(f"del fitness{str(self.myID)}.txt")

    def Create_World(self):
        length, width, height = 1, 1, 1
        # tell pyrosim the name of the file where information about the world you're about to create should be stored.
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[3, 3, 0.5], size=[length, width, height])

        # close file
        pyrosim.End()

    def Create_Body(self):
        length, width, height = 1, 1, 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[length, width, height])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0, 0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position=[-0.5, 0, 1], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position=[0.5, 0, 1], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")


        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id