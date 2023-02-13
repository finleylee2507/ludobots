import os
import random
import time

import numpy as np

from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.num_links = random.randint(2, 10)
        # self.num_links=2
        self.sensor_neuron_count = 0
        self.motor_neuron_count = 0
        self.links_with_sensors = []

        # randomly asssign sensors to links
        for i in range(self.num_links):
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

        # create links
        for i in range(self.num_links):
            length, width, height = np.random.uniform(0.2, 1, 3)
            name = f"Link{i}"

            print("Link: ", name)
            if i == 0:  # first link (absolute positioning)
                pos = [-length / 2, 0, height / 2]

                # pyrosim.Send_Cube(name=name, pos=pos, size=[
                #                   length, width, height])

                if name in self.links_with_sensors:  # color links with sensor green
                    print("Painting green")
                    pyrosim.Send_Cube(
                        name=name, pos=pos, size=[length, width, height], color_name='Green', color_string='    <color rgba="0.0 128.0 1.0 1.0"/>')
                else:  # use default color for links without sensor
                    print("Painting blue")
                    pyrosim.Send_Cube(
                        name=name, pos=pos, size=[length, width, height], color_name='Blue',color_string='    <color rgba="0.0 0.0 255.0 1.0"/>')

            else:
                parent = f"Link{i - 1}"
                diff = (height / 2) - (last_height / 2)

                if i == 1:
                    # absolutely positioned joint
                    pyrosim.Send_Joint(name=f"{parent}_{name}", parent=parent, child=name, type="revolute",
                                       position=[-last_length, 0, height / 2], jointAxis="1 0 0")
                else:
                    # relatively positioned joint
                    pyrosim.Send_Joint(name=f"{parent}_{name}", parent=parent, child=name, type="revolute",
                                       position=[-last_length, 0, diff], jointAxis="1 0 0")

                if name in self.links_with_sensors:  # color links with sensor green
                    print("Painting green")
                    pyrosim.Send_Cube(
                        name=name, pos=[-length / 2, 0, 0], size=[length, width, height], color_name='Green',color_string='    <color rgba="0.0 128.0 1.0 1.0"/>')
                else:  # use default color for links without sensor
                    print("Painting blue")
                    pyrosim.Send_Cube(
                        name=name, pos=[-length / 2, 0, 0], size=[length, width, height], color_name='Blue',color_string='    <color rgba="0.0 0.0 255.0 1.0"/>')

            last_length = length
            last_height = height

        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # for i in range(self.num_links):
        #     random_num = random.uniform(0, 1)
        #     link_name = f"Link{i}"
        #     if random_num > 0.5:  # place sensor neuron
        #         pyrosim.Send_Sensor_Neuron(
        #             name=self.sensor_neuron_count, linkName=link_name)
        #         self.sensor_neuron_count += 1

        for link_name in self.links_with_sensors:
            pyrosim.Send_Sensor_Neuron(
                name=self.sensor_neuron_count, linkName=link_name)
            self.sensor_neuron_count += 1

        for i in range(1, self.num_links):
            curr = f"Link{i}"
            parent = f"Link{i - 1}"
            joint_name = f"{parent}_{curr}"
            pyrosim.Send_Motor_Neuron(
                name=self.sensor_neuron_count + i-1, jointName=joint_name)
            self.motor_neuron_count += 1

        print("Num sensor: ", self.sensor_neuron_count,
              " Num motor: ", self.motor_neuron_count)
        # self.weights = np.random.rand(self.sensor_neuron_count, self.motor_neuron_count) * 2 - 1

        # connect sensor neurons to motor neurons
        for currentRow in range(0, self.sensor_neuron_count):
            for currentColumn in range(0, self.motor_neuron_count):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + self.sensor_neuron_count,
                                     weight=1)

        pyrosim.End()

    def Mutate(self):
        pass
        # randomRow = random.randint(0, self.sensor_neuron_count - 1)
        # randomColumn = random.randint(0, self.motor_neuron_count - 1)
        # self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id
