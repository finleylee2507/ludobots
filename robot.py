import os
import pybullet as p
import constants as c
import pyrosim.pyrosim as pyrosim
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR


class ROBOT:

    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF(f"body{solutionID}.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f"del brain{solutionID}.nndf")
        os.system(f"del body{solutionID}.urdf")

    # generate the sensors
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    # tell each sensor to check its value
    def Sense(self, time):

        for key in self.sensors:
            self.sensors[key].Get_Value(time)

    # generate the motors
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    # move joints based on motor neuron values
    def Act(self, time):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        # stateOfLinkZero = p.getLinkState(self.robotId, 0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]

        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xCoordinateOfLinkZero = basePosition[0]
        fitness=xCoordinateOfLinkZero*-1 #flip so we get a positive value
        # print("State of link zero: ", stateOfLinkZero)
        # print("Position of link zero: ", positionOfLinkZero)
        # print("X: ", xCoordinateOfLinkZero)

        f = open(f"./tmp{self.solutionID}.txt", "w")
        f.write(str(fitness))
        f.close()

        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
