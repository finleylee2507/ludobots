import os
import random
import time

import numpy as np

from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.linkNames = []
        self.jointNames = []

        # self.num_links_x = random.randint(3, 20)
        # # self.num_links = 2
        # self.sensor_neuron_count = 0
        # self.motor_neuron_count = 0
        # self.links_with_sensors = ['Link0']  # the head always has sensor on it
        # self.weights = []
        #
        # # randomly asssign sensors to links
        # for i in range(1, self.num_links_x):
        #     random_num = random.uniform(0, 1)
        #     link_name = f"Link{i}"
        #     if random_num > 0.4:
        #         self.links_with_sensors.append(link_name)
        #
        #
        # print("selected: ", self.links_with_sensors)

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


    def Expand_In_Direction(self,num_links,child_link,child_link_dimensions,direction):

        # Given a child node, expand in the specified direction
        #direction: 0=>+x, 1=>-x, 2=>
        link_sizes = [(random.uniform(0.2, 1.2), random.uniform(0.2, 1.2), random.uniform(0.2, 1.2))]

        # if direction == "+x":
        #     link_name_string = "XLink"
        #     joint_posn = [linksize_x / 2, linksize_y / 2, 0]
        #     joint_axis = "1 0 0"
        #     link_posn = [linksize[0] / 2, 0, 0]
        # elif direction == "-x":
        #     link_name_string = "MinXLink"
        #     joint_posn = [-0.5 * linksize_x, linksize_y / 2, 0]
        #     joint_axis = "1 0 0"
        #     link_posn = [-0.5 * linksize[0], 0, 0]
        # elif direction == "+z":
        #     link_name_string = "ZLink"
        #     joint_posn = [0, linksize_y / 2, linksize_z / 2]
        #     joint_axis = "0 0 1"
        #     link_posn = [0, 0, linksize[2] / 2]

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # first generate links in the x direction
        num_links_x = random.randint(1, 10)

        # Generate random sizes for each link
        link_sizes = [(random.uniform(0.2, 1.8), random.uniform(0.2, 1.8), random.uniform(0.2, 1.8)) for i in
                      range(num_links_x)]

        # Create root link (absolute positioning)
        root_link_size = link_sizes[0]
        pyrosim.Send_Cube(name="Link0", pos=[0, 0, root_link_size[2] / 2], size=root_link_size, isSensor=False)

        # Generate all other links and joints
        prev_link_name = "Link0"
        for i in range(1, num_links_x):
            link_size = link_sizes[i]
            link_name = f"Link{i}"
            joint_name = f"{prev_link_name}_{link_name}"

            # Determine joint position
            if i == 1: #use absolute positioning
                joint_pos_x = root_link_size[0] / 2
                joint_pos_z = max([size[2] for size in link_sizes]) / 2
            else: #use relative positioning
                joint_pos_x = prev_link_size[0]
                joint_pos_z = 0

            # Send joint and cube
            pyrosim.Send_Joint(name=joint_name, parent=prev_link_name, child=link_name, type="revolute",
                               position=[joint_pos_x, 0, joint_pos_z], jointAxis="1 0 0")
            is_sensor=random.choice([True,False])
            if is_sensor:
                self.linkNames.append(link_name)
                self.jointNames.append(joint_name)
            pyrosim.Send_Cube(name=link_name, pos=[link_size[0]/2, 0, 0], size=link_size,
                              isSensor=is_sensor)

            prev_link_name = link_name
            prev_link_size = link_size



        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # for link_name in self.links_with_sensors:
        #     pyrosim.Send_Sensor_Neuron(
        #         name=self.sensor_neuron_count, linkName=link_name)
        #     self.sensor_neuron_count += 1
        #
        # for i in range(1, self.num_links_x):
        #     curr = f"Link{i}"
        #     parent = f"Link{i - 1}"
        #     joint_name = f"{parent}_{curr}"
        #     pyrosim.Send_Motor_Neuron(
        #         name=self.sensor_neuron_count + i - 1, jointName=joint_name)
        #     self.motor_neuron_count += 1
        #
        # print("Num sensor: ", self.sensor_neuron_count,
        #       " Num motor: ", self.motor_neuron_count)
        # self.weights = np.random.rand(self.sensor_neuron_count, self.motor_neuron_count) * 2 - 1
        #
        # # connect sensor neurons to motor neurons
        # for currentRow in range(0, self.sensor_neuron_count):
        #     for currentColumn in range(0, self.motor_neuron_count):
        #         pyrosim.Send_Synapse(sourceNeuronName=currentRow,
        #                              targetNeuronName=currentColumn + self.sensor_neuron_count,
        #                              weight=self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Mutate(self):
        pass
        # randomRow = random.randint(0, self.sensor_neuron_count - 1)
        # randomColumn = random.randint(0, self.motor_neuron_count - 1)
        # self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id
