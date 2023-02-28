import time

import pybullet as p
import pybullet_data

import constants
from robot import ROBOT
from world import WORLD


class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # add gravity
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    # destructor
    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(constants.simulationSteps):
            if self.directOrGUI == "GUI":
                time.sleep(1 / 60)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
