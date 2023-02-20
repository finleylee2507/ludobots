import os
import random
import time

import numpy as np

from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.num_links = random.randint(3, 20)
        # self.num_links = 2
        self.sensor_neuron_count = 0
        self.motor_neuron_count = 0
        self.links_with_sensors = ['Link0']  # the head always has sensor on it
        self.weights = []

        # randomly asssign sensors to links
        for i in range(1, self.num_links):
            random_num = random.uniform(0, 1)
            link_name = f"Link{i}"
            if random_num > 0.4:
                self.links_with_sensors.append(link_name)
                

        print("selected: ", self.links_with_sensors)

    def Evaluate(self, directOrGUI):
        pass

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Brain()
        self.Create_Body()
        os.system("start /B python simulate.py " +
                  directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"./fitness{str(self.myID)}.txt"):
            time.sleep(0.01)

        fitnessFile = open(f"./fitness{str(self.myID)}.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system(f"del fitness{str(self.myID)}.txt")

    def Create_World(self):
        length, width, height = 1, 1, 1
        # tell pyrosim the name of the file where information about the world you're about to create should be stored.
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[3, 3, 0.5], size=[
                          length, width, height])

        # close file
        pyrosim.End()

    def Create_Body(self):

        pyrosim.Start_URDF("body.urdf")

        length, width, height = np.random.uniform(0.2, 1, 3)
        currPos = [0, 0, 1+height/2]

        # first link
        if "Link0" in self.links_with_sensors:  # with sensor
            pyrosim.Send_Cube(name="Link0", pos=currPos, size=[
                              length, width, height], color_name='Green', color_string='    <color rgba="0.0 128.0 1.0 1.0"/>')
        else:
            pyrosim.Send_Cube(name="Link0", pos=currPos, size=[
                              length, width, height], color_name='Blue', color_string='    <color rgba="0.0 0.0 255.0 1.0"/>')

        # first joint
        pyrosim.Send_Joint(
            name="Link0_Link1",
            parent="Link0",
            child="Link1",
            type="revolute",
            position=[length / 2, 0, 1 + height],
            jointAxis="0 1 0"
        )

        # second link
        length, width, height == np.random.uniform(
            0.2, 1, 3)
        if "Link1" in self.links_with_sensors:
            pyrosim.Send_Cube(name="Link1", pos=[length/2, 0, -height/2], size=[
                              length, width, height], color_name='Green', color_string='    <color rgba="0.0 128.0 1.0 1.0"/>')

        else:
            pyrosim.Send_Cube(name="Link1", pos=[length/2, 0, -height/2], size=[
                length, width, height], color_name='Blue', color_string='    <color rgba="0.0 0.0 255.0 1.0"/>')

        c = [length/2, 0, -height/2]
        lastLength = length
        lastWidth = width
        lastHeight = height

        for i in range(2, self.num_links):
            direction = random.randint(0, 7)
            length, width, height = np.random.uniform(0.2, 1, 3)
            curr_name = f"Link{i}"
            parent_name = f"Link{i-1}"

            if curr_name in self.links_with_sensors:
                color_name = 'Green'
                color_string = '    <color rgba="0.0 128.0 1.0 1.0"/>'
            else:
                color_name = 'Blue'
                color_string = '    <color rgba="0.0 0.0 255.0 1.0"/>'

            if direction in [0, 1]:  # forward
                if direction == 0:  # forward up
                    pos = [length / 2, 0, -height / 2]
                else:  # forward down
                    pos = [length / 2, 0, height / 2]
                joint_axis = "0 1 0"
                pos1 = [c[0] + lastLength / 2, c[1], c[2] + lastHeight / 2]
                c = [pos[0], pos[1], pos[2]]
            elif direction in [2, 3]:  # right
                if direction == 2:  # right up
                    pos = [0, width / 2, -height / 2]
                else:  # right down
                    pos = [0, width / 2, height / 2]
                joint_axis = "1 0 0"
                pos1 = [c[0], c[1] + lastWidth / 2, c[2] + lastHeight / 2]
                c = [pos[0], pos[1], pos[2]]
            elif direction in [4, 5]:  # backward
                if direction == 4:  # backward down
                    pos = [-length / 2, 0, -height / 2]
                else:  # backward up
                    pos = [-length / 2, 0, height / 2]
                joint_axis = "0 1 0"
                pos1 = [c[0] - lastLength / 2, c[1], c[2] + lastHeight / 2]
                c = [pos[0], pos[1], pos[2]]
            else:  # left
                if direction == 6:  # left down
                    pos = [0, -width / 2, -height / 2]
                else:  # left up
                    pos = [0, -width / 2, height / 2]
                joint_axis = "1 0 0"
                pos1 = [c[0], c[1] - lastWidth / 2, c[2] + lastHeight / 2]
                c = [pos[0], pos[1], pos[2]]

            pyrosim.Send_Joint(
                name=f"{parent_name}_{curr_name}",
                parent=parent_name,
                child=curr_name,
                type="revolute",
                position=pos1,
                jointAxis=joint_axis
            )

            pyrosim.Send_Cube(
                name=curr_name,
                pos=pos,
                size=[length, width, height],
                color_name=color_name,
                color_string=color_string
            )

            # update last dimensions so they can be referred to in the next iteration
            lastLength = length
            lastWidth = width
            lastHeight = height

        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for link_name in self.links_with_sensors:
            pyrosim.Send_Sensor_Neuron(
                name=self.sensor_neuron_count, linkName=link_name)
            self.sensor_neuron_count+=1 

        for i in range(1, self.num_links):
            curr = f"Link{i}"
            parent = f"Link{i - 1}"
            joint_name = f"{parent}_{curr}"
            pyrosim.Send_Motor_Neuron(
                name=self.sensor_neuron_count + i-1, jointName=joint_name)
            self.motor_neuron_count += 1

        print("Num sensor: ", self.sensor_neuron_count,
              " Num motor: ", self.motor_neuron_count)
        self.weights = np.random.rand(self.sensor_neuron_count, self.motor_neuron_count) * 2 - 1

       
        # connect sensor neurons to motor neurons
        for currentRow in range(0, self.sensor_neuron_count):
            for currentColumn in range(0, self.motor_neuron_count):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + self.sensor_neuron_count,
                                     weight=self.weights[currentRow,currentColumn])

        pyrosim.End()

    def Mutate(self):
        pass
        # randomRow = random.randint(0, self.sensor_neuron_count - 1)
        # randomColumn = random.randint(0, self.motor_neuron_count - 1)
        # self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id
