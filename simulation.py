import time

import pybullet as p
import pybullet_data

from robot import ROBOT
from world import WORLD


class SIMULATION:

    def __init__(self):
        print("simulation created")
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
        for i in range(1000):
            time.sleep(1 / 240)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
