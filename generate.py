import random

import pyrosim.pyrosim as pyrosim

length, width, height = 1, 1, 1


def Create_World():
    # tell pyrosim the name of the file where information about the world you're about to create should be stored.
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[3, 3, 0.5], size=[length, width, height])

    # close file
    pyrosim.End()


def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                       position=[2, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                       position=[1, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])

    pyrosim.End()


def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for i in range(0, 3):
        for j in range(3, 5):
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=random.random()*2-1)

    # pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=3, weight=2.0)
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=2.0)
    # pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=2.0)
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)
    # pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=2.0)
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=2.0)

    pyrosim.End()


Create_World()
Generate_Body()
Generate_Brain()

