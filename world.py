import pybullet as p


class WORLD:
    def __int__(self):
        # set floor
        self.planeId = p.loadURDF("plane.urdf")

        # read in the world described in box.sdf
        p.loadSDF("world.sdf")
