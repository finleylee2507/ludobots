import pyrosim.pyrosim as pyrosim


x, y, z = 0, 0, 0.5
length, width, height = 1, 1, 1

def Create_World():
    # tell pyrosim the name of the file where information about the world you're about to create should be stored.
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[x+3, y+3, z], size=[length, width, height])

    # close file
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])
    pyrosim.End()

Create_World()
Create_Robot()


