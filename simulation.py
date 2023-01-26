import time

import pybullet as p
import pybullet_data

from robot import ROBOT
from world import WORLD


class SIMULATION:

    def __init__(self, directOrGUI):

        self.directOrGUI=directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # add gravity
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    # destructor
    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(500):
            if self.directOrGUI=="GUI":
                time.sleep(1 / 240)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
