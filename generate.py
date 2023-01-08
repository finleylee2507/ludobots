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
    pyrosim.Send_Cube(name="BackLeg", pos=[0.5, 0, 0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="BackLeg_Torso", parent="BackLeg", child="Torso", type="revolute",
                       position=[1, 0, 1])
    pyrosim.Send_Cube(name="Torso", pos=[0.5, 0, 0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                       position=[1, 0, 0])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5], size=[length, width, height])

    pyrosim.End()


Create_World()
Create_Robot()
