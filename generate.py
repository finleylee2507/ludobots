import pyrosim.pyrosim as pyrosim

# tell pyrosim the name of the file where information about the world you're about to create should be stored.
pyrosim.Start_SDF("boxes.sdf")

x, y, = 0, 0

# store a box with initial position and dimension

for row in range(5):
    for col in range(5):
        length, width, height = 1, 1, 1
        z = 0.5
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[row, col, z], size=[length, width, height])
            z += height
            length *= 0.9
            width *= 0.9
            height *= 0.9

# pyrosim.Send_Cube(name="Box", pos=[x1,y1,z1], size=[length, width, height])
# pyrosim.Send_Cube(name="Box2", pos=[x2,y2,z2], size=[length, width, height])
# close file
pyrosim.End()
