import pyrosim.pyrosim as pyrosim

# tell pyrosim the name of the file where information about the world you're about to create should be stored.
pyrosim.Start_SDF("box.sdf")

# store a box with initial position x=0, y=0, z=0.5, and length, width and height all equal to 1 meter, in box.sdf.
pyrosim.Send_Cube(name="Box", pos=[0, 0, 0.5], size=[1, 1, 1])

#close file
pyrosim.End()
