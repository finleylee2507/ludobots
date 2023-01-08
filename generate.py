import pyrosim.pyrosim as pyrosim

length, width, height = 1, 1, 1


def Create_World():
    # tell pyrosim the name of the file where information about the world you're about to create should be stored.
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[3, 3, 0.5], size=[length, width, height])

    # close file
    pyrosim.End()


def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Link0", pos=[0, 0, 0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute",
                       position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link1", pos=[0, 0, 0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute",
                       position=[0, 0, 1])
    pyrosim.Send_Cube(name="Link2", pos=[0, 0, 0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute",
                       position=[0, 0.5, 0.5])
    pyrosim.Send_Cube(name="Link3", pos=[0, 0.5, 0], size=[length, width, height])
    pyrosim.End()


Create_World()
Create_Robot()
