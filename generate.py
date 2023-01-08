import pyrosim.pyrosim as pyrosim

# tell pyrosim the name of the file where information about the world you're about to create should be stored.
pyrosim.Start_SDF("boxes.sdf")

length,width,height=1,1,1

x1,y1,z1=0,0,0.5
x2,y2,z2=1,0,1.5
# store a box with initial position and dimension
pyrosim.Send_Cube(name="Box", pos=[x1,y1,z1], size=[length, width, height])
pyrosim.Send_Cube(name="Box2", pos=[x2,y2,z2], size=[length, width, height])
#close file
pyrosim.End()
