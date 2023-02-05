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

    # def Create_Body(self):
    #     length, width, height = 1, 1, 1
    #     pyrosim.Start_URDF("body.urdf")
    #     pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[length, width, height])
    #     pyrosim.Send_Joint(name="Torso_FrontLeg1", parent="Torso", child="FrontLeg1", type="revolute",
    #                        position=[0.25, 0.5, 1], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLeg1", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_FrontLeg2", parent="Torso", child="FrontLeg2", type="revolute",
    #                        position=[-0.25, 0.5, 1], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLeg2", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_FrontLeg3", parent="Torso", child="FrontLeg3", type="revolute",
    #                        position=[0, 0.5, 1.5], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLeg3", pos=[0, 1, 0], size=[0.2, 2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_BackLeg1", parent="Torso", child="BackLeg1", type="revolute",
    #                        position=[0.25, -0.5, 1], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLeg1", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_BackLeg2", parent="Torso", child="BackLeg2", type="revolute",
    #                        position=[-0.25, -0.5, 1], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLeg2", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_BackLeg3", parent="Torso", child="BackLeg3", type="revolute",
    #                        position=[0, -0.5, 1.5], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLeg3", pos=[0, -1, 0], size=[0.2, 2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_LeftLeg1", parent="Torso", child="LeftLeg1", type="revolute",
    #                        position=[-0.5, 0.25, 1], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="LeftLeg1", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_LeftLeg2", parent="Torso", child="LeftLeg2", type="revolute",
    #                        position=[-0.5, -0.25, 1], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="LeftLeg2", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_LeftLeg3", parent="Torso", child="LeftLeg3", type="revolute",
    #                        position=[-0.5, 0, 1.5], jointAxis="0 1 0")
    #     #
    #     pyrosim.Send_Cube(name="LeftLeg3", pos=[-1, 0, 0], size=[2, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_RightLeg1", parent="Torso", child="RightLeg1", type="revolute",
    #                        position=[0.5, 0.25, 1], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLeg1", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_RightLeg2", parent="Torso", child="RightLeg2", type="revolute",
    #                        position=[0.5, -0.25, 1], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLeg2", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="Torso_RightLeg3", parent="Torso", child="RightLeg3", type="revolute",
    #                        position=[0.5, 0, 1.5], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLeg3", pos=[1, 0, 0], size=[2, 0.2, 0.2])
    #
    #     pyrosim.Send_Joint(name="FrontLeg1_FrontLowerLeg1", parent="FrontLeg1", child="FrontLowerLeg1", type="revolute",
    #                        position=[0, 1, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLowerLeg1", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="FrontLeg2_FrontLowerLeg2", parent="FrontLeg2", child="FrontLowerLeg2", type="revolute",
    #                        position=[0, 1, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLowerLeg2", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="FrontLeg3_FrontLowerLeg3", parent="FrontLeg3", child="FrontLowerLeg3", type="revolute",
    #                        position=[0, 2, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="FrontLowerLeg3", pos=[0, 0, -(1.5 / 2)], size=[0.2, 0.2, 1.5])
    #
    #     pyrosim.Send_Joint(name="BackLeg1_BackLowerLeg1", parent="BackLeg1", child="BackLowerLeg1", type="revolute",
    #                        position=[0, -1, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLowerLeg1", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="BackLeg2_BackLowerLeg2", parent="BackLeg2", child="BackLowerLeg2", type="revolute",
    #                        position=[0, -1, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLowerLeg2", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="BackLeg3_BackLowerLeg3", parent="BackLeg3", child="BackLowerLeg3", type="revolute",
    #                        position=[0, -2, 0], jointAxis="1 0 0")
    #     pyrosim.Send_Cube(name="BackLowerLeg3", pos=[0, 0, -1.5 / 2], size=[0.2, 0.2, 1.5])
    #
    #     pyrosim.Send_Joint(name="LeftLeg1_LeftLowerLeg1", parent="LeftLeg1", child="LeftLowerLeg1", type="revolute",
    #                        position=[-1, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="LeftLowerLeg1", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #     pyrosim.Send_Joint(name="LeftLeg2_LeftLowerLeg2", parent="LeftLeg2", child="LeftLowerLeg2", type="revolute",
    #                        position=[-1, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="LeftLowerLeg2", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="LeftLeg3_LeftLowerLeg3", parent="LeftLeg3", child="LeftLowerLeg3", type="revolute",
    #                        position=[-2, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="LeftLowerLeg3", pos=[0, 0, -1.5 / 2], size=[0.2, 0.2, 1.5])
    #
    #     pyrosim.Send_Joint(name="RightLeg1_RightLowerLeg1", parent="RightLeg1", child="RightLowerLeg1", type="revolute",
    #                        position=[1, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLowerLeg1", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #     pyrosim.Send_Joint(name="RightLeg2_RightLowerLeg2", parent="RightLeg2", child="RightLowerLeg2", type="revolute",
    #                        position=[1, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLowerLeg2", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
    #
    #     pyrosim.Send_Joint(name="RightLeg3_RightLowerLeg3", parent="RightLeg3", child="RightLowerLeg3", type="revolute",
    #                        position=[2, 0, 0], jointAxis="0 1 0")
    #
    #     pyrosim.Send_Cube(name="RightLowerLeg3", pos=[0, 0, -1.5 / 2], size=[0.2, 0.2, 1.5])
    #
    #     pyrosim.End()
    #
    # def Create_Brain(self):
    #     pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
    #     # Sensor neurons
    #     # pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    #     # pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLeg1")
    #     # pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg2")
    #     # pyrosim.Send_Sensor_Neuron(name=3, linkName="FrontLeg3")
    #     # pyrosim.Send_Sensor_Neuron(name=4, linkName="BackLeg1")
    #     # pyrosim.Send_Sensor_Neuron(name=5, linkName="BackLeg2")
    #     # pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLeg3")
    #     # pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLeg1")
    #     # pyrosim.Send_Sensor_Neuron(name=8, linkName="LeftLeg2")
    #     # pyrosim.Send_Sensor_Neuron(name=9, linkName="LeftLeg3")
    #     # pyrosim.Send_Sensor_Neuron(name=10, linkName="RightLeg1")
    #     # pyrosim.Send_Sensor_Neuron(name=11, linkName="RightLeg2")
    #     # pyrosim.Send_Sensor_Neuron(name=12, linkName="RightLeg3")
    #     pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg1")
    #     pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLowerLeg2")
    #     pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLowerLeg3")
    #     pyrosim.Send_Sensor_Neuron(name=3, linkName="BackLowerLeg1")
    #     pyrosim.Send_Sensor_Neuron(name=4, linkName="BackLowerLeg2")
    #     pyrosim.Send_Sensor_Neuron(name=5, linkName="BackLowerLeg3")
    #     pyrosim.Send_Sensor_Neuron(name=6, linkName="LeftLowerLeg1")
    #     pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg2")
    #     pyrosim.Send_Sensor_Neuron(name=8, linkName="LeftLowerLeg3")
    #     pyrosim.Send_Sensor_Neuron(name=9, linkName="RightLowerLeg1")
    #     pyrosim.Send_Sensor_Neuron(name=10, linkName="RightLowerLeg2")
    #     pyrosim.Send_Sensor_Neuron(name=11, linkName="RightLowerLeg3")
    #
    #     # Motor Neurons
    #     pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_FrontLeg1")
    #     pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_FrontLeg2")
    #     pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_FrontLeg3")
    #     pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_BackLeg1")
    #     pyrosim.Send_Motor_Neuron(name=16, jointName="Torso_BackLeg2")
    #     pyrosim.Send_Motor_Neuron(name=17, jointName="Torso_BackLeg3")
    #     pyrosim.Send_Motor_Neuron(name=18, jointName="Torso_LeftLeg1")
    #     pyrosim.Send_Motor_Neuron(name=19, jointName="Torso_LeftLeg2")
    #     pyrosim.Send_Motor_Neuron(name=20, jointName="Torso_LeftLeg3")
    #     pyrosim.Send_Motor_Neuron(name=21, jointName="Torso_RightLeg1")
    #     pyrosim.Send_Motor_Neuron(name=22, jointName="Torso_RightLeg2")
    #     pyrosim.Send_Motor_Neuron(name=23, jointName="Torso_RightLeg3")
    #     pyrosim.Send_Motor_Neuron(name=24, jointName="FrontLeg1_FrontLowerLeg1")
    #     pyrosim.Send_Motor_Neuron(name=25, jointName="FrontLeg2_FrontLowerLeg2")
    #     pyrosim.Send_Motor_Neuron(name=26, jointName="FrontLeg3_FrontLowerLeg3")
    #     pyrosim.Send_Motor_Neuron(name=27, jointName="BackLeg1_BackLowerLeg1")
    #     pyrosim.Send_Motor_Neuron(name=28, jointName="BackLeg2_BackLowerLeg2")
    #     pyrosim.Send_Motor_Neuron(name=29, jointName="BackLeg3_BackLowerLeg3")
    #     pyrosim.Send_Motor_Neuron(name=30, jointName="LeftLeg1_LeftLowerLeg1")
    #     pyrosim.Send_Motor_Neuron(name=31, jointName="LeftLeg2_LeftLowerLeg2")
    #     pyrosim.Send_Motor_Neuron(name=32, jointName="LeftLeg3_LeftLowerLeg3")
    #     pyrosim.Send_Motor_Neuron(name=33, jointName="RightLeg1_RightLowerLeg1")
    #     pyrosim.Send_Motor_Neuron(name=34, jointName="RightLeg1_RightLowerLeg1")
    #     pyrosim.Send_Motor_Neuron(name=35, jointName="RightLeg2_RightLowerLeg2")
    #     pyrosim.Send_Motor_Neuron(name=36, jointName="RightLeg3_RightLowerLeg3")
    #
    #     for currentRow in range(0, c.numSensorNeurons):
    #         for currentColumn in range(0, c.numMotorNeurons):
    #             pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
    #                                  weight=self.weights[currentRow][currentColumn])
    #
    #     pyrosim.End()

    def Create_Body(self):
        length = 3
        width = 2
        height = 0.4
        pyrosim.Start_URDF("body.urdf")

        # Torso
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2.25], size=[length, width, height])

        #Head
        pyrosim.Send_Joint(name="Torso_Head", parent="Torso", child="Head", type="revolute",
                           position=[0,0,2.25], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Head", pos=[0, 0,0.5], size=[0.5, 0.5, 1])

        pyrosim.Send_Joint(name="Head_LeftEar", parent="Head", child="LeftEar", type="revolute",
                           position=[0, 0, 0.5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftEar", pos=[0, -0.1, 0.5], size=[0.1, 0.1, 0.5])

        pyrosim.Send_Joint(name="Head_RightEar", parent="Head", child="RightEar", type="revolute",
                           position=[0, 0, 0.5], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightEar", pos=[0, 0.1, 0.5], size=[0.1, 0.1, 0.5])
        # Front leg
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[-0.5, 0, 2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, -0.5, 0], size=[.2, .2, .5])
        pyrosim.Send_Joint(name="FrontLeg_LowerFrontLeg", parent="FrontLeg", child="LowerFrontLeg", type="revolute",
                           position=[-0.1, -0.5, -0.25], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[-0.1, 0, -0.25], size=[.2, .2, .5])

        # Back leg
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0.5, 0, 2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[.2, .2, .5])
        pyrosim.Send_Joint(name="BackLeg_LowerBackLeg", parent="BackLeg", child="LowerBackLeg", type="revolute",
                           position=[0.1, -0.5, -0.2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0.1, 0, -0.25], size=[.2, .2, .5])

        # Left Leg
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position=[-0.5, 0, 2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0, 0.5, 0], size=[.2, .2, .5])
        pyrosim.Send_Joint(name="LeftLeg_LowerLeftLeg", parent="LeftLeg", child="LowerLeftLeg", type="revolute",
                           position=[-0.1, 0.5, -0.2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[-0.1, 0, -0.25], size=[.2, .2, .5])

        # Right leg
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position=[0.5, 0, 2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0, 0.5, 0], size=[.2, .2, .5])
        pyrosim.Send_Joint(name="RightLeg_LowerRightLeg", parent="RightLeg", child="LowerRightLeg", type="revolute",
                           position=[0.1, 0.5, -0.2], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0.1, 0, -0.25], size=[.2, .2, .5])



        pyrosim.End()
        while not os.path.exists('body.urdf'):
            time.sleep(0.01)

        # Generates neural network, writes out to file

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Sensor neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName='LowerFrontLeg')
        pyrosim.Send_Sensor_Neuron(name=3, linkName='LowerLeftLeg')
        pyrosim.Send_Sensor_Neuron(name=4, linkName='LowerRightLeg')


        # Motor neurons
        pyrosim.Send_Motor_Neuron(name=8, jointName='Torso_BackLeg')
        pyrosim.Send_Motor_Neuron(name=9, jointName='Torso_FrontLeg')
        pyrosim.Send_Motor_Neuron(name=10, jointName='Torso_LeftLeg')
        pyrosim.Send_Motor_Neuron(name=11, jointName='Torso_RightLeg')
        pyrosim.Send_Motor_Neuron(name=12, jointName='BackLeg_LowerBackLeg')
        pyrosim.Send_Motor_Neuron(name=13, jointName='FrontLeg_LowerFrontLeg')
        pyrosim.Send_Motor_Neuron(name=14, jointName='LeftLeg_LowerLeftLeg')
        pyrosim.Send_Motor_Neuron(name=15, jointName='RightLeg_LowerRightLeg')



        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentColumn])



        pyrosim.End()
        while not os.path.exists('brain' + str(self.myID) + '.nndf'):
            time.sleep(0.01)


    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * (c.numSensorNeurons - 1) - (c.numMotorNeurons - 1)
    def Set_ID(self, id):
        self.myID = id
