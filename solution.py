import os
import random
import time

import numpy as np

from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.linksWithSensor = []
        self.jointNames = []
        self.weights = []

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
        self.Create_Body()
        self.Create_Brain()

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
        # pyrosim.Send_Cube(name="Box", pos=[3, 3, 0.5], size=[
        #     length, width, height])

        # close file
        pyrosim.End()

    def Expand_In_Direction(self, num_links, child_link, child_link_dimensions, direction):

        # Given a child node, expand in the specified direction
        # direction: 0=>+x, 1=>-x, 2=>+z
        link_size = [random.uniform(0.2, 1.2), random.uniform(0.2, 1.2), random.uniform(0.2, 1.2)]

        prev_link_size = link_size

        # sepcify joint and link positions
        if direction == 0:
            link_name = "ZeroLink"
            joint_pos = [child_link_dimensions[0] / 2, child_link_dimensions[1] / 2, 0]
            joint_axis = "1 0 0"
            link_pos = [link_size[0] / 2, 0, 0]
        elif direction == 1:
            link_name = "OneLink"
            joint_pos = [-1 * child_link_dimensions[0] / 2, child_link_dimensions[1] / 2, 0]
            joint_axis = "1 0 0"
            link_pos = [-1 * link_size[0] / 2, 0, 0]
        elif direction == 2:
            link_name = "TwoLink"
            joint_pos = [0, child_link_dimensions[1] / 2, child_link_dimensions[2] / 2]
            joint_axis = "0 0 1"
            link_pos = [0, 0, link_size[2] / 2]

        for i in range(num_links):
            if i == 0:  # first branch joint (absolute positioning)
                parent_name = child_link

            else:  # relative positioning for the rest
                if direction == 0:
                    joint_pos = [prev_link_size[0], 0, 0]
                elif direction == 1:
                    joint_pos = [-1 * prev_link_size[0], 0, 0]
                elif direction == 2:
                    joint_pos = [0, 0, prev_link_size[2]]

                parent_name = f"{child_link}{link_name}{i - 1}"

            child_name = f"{child_link}{link_name}{i}"

            pyrosim.Send_Joint(name=f"{parent_name}_{child_name}",
                               parent=parent_name, child=child_name,
                               type="revolute",
                               position=[joint_pos[0], joint_pos[1], joint_pos[2]],
                               jointAxis=joint_axis)

            sensor_boolean = random.choice([True, False])

            if sensor_boolean:
                self.linksWithSensor.append(child_name)

            self.jointNames.append(f"{parent_name}_{child_name}")

            pyrosim.Send_Cube(name=child_name,
                              pos=[link_pos[0], link_pos[1], link_pos[2]],
                              size=[link_size[0], link_size[1], link_size[2]],
                              isSensor=sensor_boolean)

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # first generate links in the +y direction
        num_links_y = random.randint(3, 8)

        # Generate random sizes for each link
        link_sizes = [[random.uniform(0.2, 1.8), random.uniform(0.2, 1.8), random.uniform(0.2, 1.8)] for i in
                      range(num_links_y)]

        # Create root link (absolute positioning)
        root_link_size = link_sizes[0]
        pyrosim.Send_Cube(name="Link0", pos=[0, 0, root_link_size[2] / 2], size=root_link_size, isSensor=False)

        # Generate all other links and joints
        prev_link_name = "Link0"
        for i in range(1, num_links_y):
            link_size = link_sizes[i]
            link_name = f"Link{i}"
            joint_name = f"{prev_link_name}_{link_name}"

            # Determine joint position
            if i == 1:  # use absolute positioning
                joint_pos_y = root_link_size[1] / 2
                joint_pos_z = max([size[2] for size in link_sizes]) / 2
            else:  # use relative positioning
                joint_pos_y = prev_link_size[1]
                joint_pos_z = 0

            # Send joint and cube
            pyrosim.Send_Joint(name=joint_name, parent=prev_link_name, child=link_name, type="revolute",
                               position=[0, joint_pos_y, joint_pos_z], jointAxis="1 0 0")
            is_sensor = random.choice([True, False])
            if is_sensor:
                self.linksWithSensor.append(link_name)

            self.jointNames.append(joint_name)
            pyrosim.Send_Cube(name=link_name, pos=[0, link_size[1] / 2, 0], size=link_size,
                              isSensor=is_sensor)

            prev_link_name = link_name
            prev_link_size = link_size

            # expand in different directions with randomly selected number of links 

            # +x direction
            self.Expand_In_Direction(random.randint(0, 2), link_name, link_size, 0)
            # -x direction
            self.Expand_In_Direction(random.randint(0, 2), link_name, link_size, 1)

            # +z direction
            self.Expand_In_Direction(random.randint(0, 5), link_name, link_size, 2)
        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        print("Sensors: ", self.linksWithSensor)
        print("Joints: ", self.jointNames)

        # initialize weights array
        self.weights = np.random.rand(len(self.linksWithSensor), len(self.jointNames)) * 2 - 1

        # attach sensors to links with sensors
        counter = 0
        for i in range(len(self.linksWithSensor)):
            pyrosim.Send_Sensor_Neuron(
                name=i, linkName=self.linksWithSensor[i])
            counter += 1

        # attach motors to all joints
        for i in range(len(self.jointNames)):
            pyrosim.Send_Motor_Neuron(
                name=counter + i, jointName=self.jointNames[i])

        # connect sensor neurons to motor neurons through synapse
        for currentRow in range(len(self.linksWithSensor)):
            for currentColumn in range(len(self.jointNames)):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + len(self.linksWithSensor),
                                     weight=self.weights[currentRow][currentColumn])

    
        pyrosim.End()

    def Mutate(self):
        pass
        # randomRow = random.randint(0, self.sensor_neuron_count - 1)
        # randomColumn = random.randint(0, self.motor_neuron_count - 1)
        # self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id
