import os

import pybullet as p

import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
import constants as c


class ROBOT:
    def __init__(self,solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID=solutionID
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")

        os.system(f"del brain{solutionID}.nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            # This results in the SENSOR's constructor being called three times. Each time, it returns an instance of
            # SENSOR. That instance is stored as an entry in the self.sensors dictionary.
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, time):

        for key in self.sensors:
            self.sensors[key].Get_Value(time)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, time):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.motorJointRange
                print("Desired angle: ", desiredAngle)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Get_Fitness(self):
        # stateOfLinkZero = p.getLinkState(self.robotId, 0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]

        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xCoordinateOfLinkZero = basePosition[0]
        # print("State of link zero: ", stateOfLinkZero)
        # print("Position of link zero: ", positionOfLinkZero)
        # print("X: ", xCoordinateOfLinkZero)

        f = open(f"./tmp{self.solutionID}.txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()

        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")


    def Think(self):
        self.nn.Update()
        # self.nn.Print()
