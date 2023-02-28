import os
import random
import time

import numpy as np

import constants
from pyrosim import pyrosim


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = []

        # Generate random values
        self.randomize()

        # controls joint axis
        self.join_axis=[]

    def randomize(self):
        self.num_links_y = 2
        self.num_expansions_x = [random.randint(
            0, 2) for _ in range(self.num_links_y)]
        self.num_expansions_neg_x = [random.randint(
            0, 2) for _ in range(self.num_links_y)]
        self.num_expansions_z = [random.randint(
            0, 2) for _ in range(self.num_links_y)]

        # randomly assign sensors to links
        self.is_sensor_y = [random.choice([True, False])
                            for _ in range(self.num_links_y)]
        self.is_sensor_x = [[random.choice([True, False]) for _ in range(self.num_expansions_x[i])] for i in
                            range(len(self.num_expansions_x))]

        self.is_sensor_neg_x = [[random.choice([True, False]) for _ in range(self.num_expansions_neg_x[i])] for i
                                in range(len(self.num_expansions_neg_x))]

        self.is_sensor_z = [[random.choice([True, False]) for j in range(self.num_expansions_z[i])] for i in
                            range(len(self.num_expansions_z))]

        # randomly assign link sizes
        self.link_sizes_y = [[random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)] for i in
                             range(self.num_links_y)]
        # find index of the tallest block and swap with first block
        max_height = max(self.link_sizes_y, key=lambda x: x[2])
        max_height_index = self.link_sizes_y.index(max_height)
        self.link_sizes_y[0], self.link_sizes_y[max_height_index] = self.link_sizes_y[max_height_index], \
            self.link_sizes_y[0]

        self.link_sizes_x = [[[random.uniform(0.2, 1.2), random.uniform(
            0.2, 0.5), random.uniform(0.2, 0.5)] for _ in range(self.num_expansions_x[i])] for i in
                             range(len(self.num_expansions_x))]

        self.link_sizes_neg_x = [[[random.uniform(0.2, 1.2), random.uniform(
            0.2, 0.5), random.uniform(0.2, 0.5)] for _ in range(self.num_expansions_neg_x[i])] for i
                                 in range(len(self.num_expansions_neg_x))]

        self.link_sizes_z = [[[random.uniform(0.2, 1.2), random.uniform(
            0.2, 0.5), random.uniform(0.2, 0.5)] for _ in range(self.num_expansions_z[i])] for i in
                             range(len(self.num_expansions_z))]
        # print("test: ",self.is_sensor_x)

    def Evaluate(self, directOrGUI):
        pass

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        if constants.supressError:
            os.system(
                f"start /B python simulate.py {directOrGUI} {self.myID} >nul 2>&1")
        else:
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

    def Expand_In_Direction(self, num_links, parent_link, parent_link_dimensions, direction, parent_link_index):

        # Given a child node, expand in the specified direction
        # direction: 0=>+x, 1=>-x, 2=>+z

        # edge case:
        if num_links == 0:
            return

        if direction == 0:
            link_sizes = self.link_sizes_x[parent_link_index]
        elif direction == 1:
            link_sizes = self.link_sizes_neg_x[parent_link_index]
        else:
            link_sizes = self.link_sizes_z[parent_link_index]
        # link_size = [random.uniform(0.2, 1.2), random.uniform(
        #     0.2, 1.2), random.uniform(0.2, 0.5)]

        prev_link_size = link_sizes[0]

        # specify joint and link positions
        if direction == 0:
            link_name = "+X"
            joint_pos = [parent_link_dimensions[0] /
                         2, parent_link_dimensions[1] / 2, 0]
            joint_axis = "0 1 0"

            link_pos = [prev_link_size[0] / 2, 0, 0]
        elif direction == 1:
            link_name = "-X"
            joint_pos = [-1 * parent_link_dimensions[0] /
                         2, parent_link_dimensions[1] / 2, 0]
            joint_axis = "0 1 0"
            link_pos = [-1 * prev_link_size[0] / 2, 0, 0]
        elif direction == 2:
            link_name = "+Z"
            joint_pos = [0, parent_link_dimensions[1] /
                         2, parent_link_dimensions[2] / 2]
            joint_axis = "0 0 1"
            link_pos = [0, 0, prev_link_size[2] / 2]

        for i in range(num_links):
            is_sensor = False
            if i == 0:  # first branch
                parent_name = parent_link

            else:  # the rest
                if direction == 0:
                    joint_pos = [prev_link_size[0], 0, 0]
                    is_sensor = self.is_sensor_x[parent_link_index][i]
                    link_pos = [link_sizes[i][0] / 2, 0, 0]
                elif direction == 1:
                    joint_pos = [-1 * prev_link_size[0], 0, 0]
                    is_sensor = self.is_sensor_neg_x[parent_link_index][i]
                    link_pos = [-1 * link_sizes[i][0] / 2, 0, 0]
                elif direction == 2:
                    joint_pos = [0, 0, prev_link_size[2]]
                    is_sensor = self.is_sensor_z[parent_link_index][i]
                    link_pos = [0, 0, link_sizes[i][2] / 2]

                parent_name = f"{parent_link}{link_name}{i - 1}"

            child_name = f"{parent_link}{link_name}{i}"

            pyrosim.Send_Joint(name=f"{parent_name}_{child_name}",
                               parent=parent_name, child=child_name,
                               type="revolute",
                               position=[joint_pos[0],
                                         joint_pos[1], joint_pos[2]],
                               jointAxis=joint_axis)

            if is_sensor:
                self.linksWithSensor.append(child_name)

            self.jointNames.append(f"{parent_name}_{child_name}")


            pyrosim.Send_Cube(name=child_name,
                              pos=[link_pos[0], link_pos[1], link_pos[2]],
                              size=[link_sizes[i][0], link_sizes[i][1], link_sizes[i][2]],
                              isSensor=is_sensor)
            prev_link_size = link_sizes[i]

    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")
        self.linksWithSensor = ["Link0"]  # the head always has sensor attached
        self.jointNames = []

        # Create head link (absolute positioning)
        head_link_size = self.link_sizes_y[0]
        pyrosim.Send_Cube(name="Link0", pos=[
            0, 0, head_link_size[2] / 2], size=head_link_size, isSensor=True)

        # Generate all other links and joints
        for i in range(1, self.num_links_y):
            link_size = self.link_sizes_y[i]
            link_name = f"Link{i}"
            prev_link_name = f"Link{i - 1}"
            joint_name = f"{prev_link_name}_{link_name}"

            # Determine joint position
            if i == 1:  # use absolute positioning
                joint_pos_y = head_link_size[1] / 2
                joint_pos_z = head_link_size[2] / 2
            else:  # use relative positioning
                joint_pos_y = prev_link_size[1]
                joint_pos_z = 0

            # Send joint and cube
            pyrosim.Send_Joint(name=joint_name, parent=prev_link_name, child=link_name, type="revolute",
                               position=[0, joint_pos_y, joint_pos_z], jointAxis="0 1 0")
            is_sensor = self.is_sensor_y[i]
            if is_sensor:
                self.linksWithSensor.append(link_name)

            self.jointNames.append(joint_name)
            pyrosim.Send_Cube(name=link_name, pos=[0, link_size[1] / 2, 0], size=link_size,
                              isSensor=is_sensor)

            prev_link_name = link_name
            prev_link_size = link_size

            # expand in different directions with randomly selected number of links

            # +x direction
            self.Expand_In_Direction(
                self.num_expansions_x[i], link_name, link_size, 0, i)
            # # -x direction
            self.Expand_In_Direction(
                self.num_expansions_neg_x[i], link_name, link_size, 1, i)

            # +z direction
            self.Expand_In_Direction(
                self.num_expansions_z[i], link_name, link_size, 2, i)

        pyrosim.End()

    def Create_Brain(self):

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # print("Sensors: ", self.linksWithSensor)
        # print("Joints: ", self.jointNames)

        # initialize weights array
        self.weights = np.random.rand(
            len(self.linksWithSensor), len(self.jointNames)) * 2 - 1

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
                                     targetNeuronName=currentColumn +
                                                      len(self.linksWithSensor),
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):

        # self.randomize()

        # pick a random weight to modify
        randomRow = random.randint(0, len(self.linksWithSensor) - 1)
        randomColumn = random.randint(0, len(self.jointNames) - 1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

        # randomly change the sensor assignment

        # self.is_sensor_y = [random.choice([True, False])
        #                     for _ in range(self.num_links_y)]
        # self.is_sensor_x = [[random.choice([True, False]) for _ in range(self.num_expansions_x[i])] for i in
        #                     range(len(self.num_expansions_x))]

        # self.is_sensor_neg_x = [[random.choice([True, False]) for _ in range(self.num_expansions_neg_x[i])] for i
        #                         in range(len(self.num_expansions_neg_x))]

        # self.is_sensor_z = [[random.choice([True, False, False]) for j in range(self.num_expansions_z[i])] for i in
        #                     range(len(self.num_expansions_z))]

        # Randomly flip a sensor value

        # For y direction
        index_to_change = random.randint(0, len(self.is_sensor_y) - 1)

        # flip the value at that index
        self.is_sensor_y[index_to_change] = not self.is_sensor_y[index_to_change]

        # X
        if self.num_expansions_x:
            i_x = random.choice(range(len(self.num_expansions_x)))
            if self.num_expansions_x[i_x]:
                j_x = random.choice(range(self.num_expansions_x[i_x]))

                self.is_sensor_x[i_x][j_x] = not self.is_sensor_x[i_x][j_x]

        # -X
        if self.num_expansions_neg_x:
            i_neg_x = random.choice(range(len(self.num_expansions_neg_x)))
            if self.num_expansions_neg_x[i_neg_x]:
                j_neg_x = random.choice(range(self.num_expansions_neg_x[i_neg_x]))
                self.is_sensor_neg_x[i_neg_x][j_neg_x] = not self.is_sensor_neg_x[i_neg_x][j_neg_x]

        # +Z
        if self.num_expansions_z:
            i_z = random.choice(range(len(self.num_expansions_z)))
            if self.num_expansions_z[i_z]:
                j_z = random.choice(range(self.num_expansions_z[i_z]))
                self.is_sensor_z[i_z][j_z] = not self.is_sensor_z[i_z][j_z]

        # Randomly change size
        options = ["link_sizes_y", "link_sizes_x", "link_sizes_neg_x", "link_sizes_z"]
        selected_option = random.choice(options)

        if selected_option == "link_sizes_y" and len(self.link_sizes_y) > 0:
            idx_y = random.randint(0, len(self.link_sizes_y) - 1)
            self.link_sizes_y[idx_y] = [random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)]

        elif selected_option == "link_sizes_x" and len(self.link_sizes_x) > 0:
            idx_x = random.randint(0, len(self.link_sizes_x) - 1)
            if len(self.link_sizes_x[idx_x]) > 0:
                subidx_x = random.randint(0, len(self.link_sizes_x[idx_x]) - 1)
                self.link_sizes_x[idx_x][subidx_x] = [random.uniform(0.2, 1.2), random.uniform(0.2, 0.5),
                                                      random.uniform(0.2, 0.5)]

        elif selected_option == "link_sizes_neg_x" and len(self.link_sizes_neg_x) > 0:
            idx_neg_x = random.randint(0, len(self.link_sizes_neg_x) - 1)
            if len(self.link_sizes_neg_x[idx_neg_x]) > 0:
                subidx_neg_x = random.randint(0, len(self.link_sizes_neg_x[idx_neg_x]) - 1)
                self.link_sizes_neg_x[idx_neg_x][subidx_neg_x] = [random.uniform(0.2, 1.2),
                                                                  random.uniform(0.2, 0.5),
                                                                  random.uniform(0.2, 0.5)]

        elif selected_option == "link_sizes_z" and len(self.link_sizes_z) > 0:
            idx_z = random.randint(0, len(self.link_sizes_z) - 1)
            if len(self.link_sizes_z[idx_z]) > 0:
                subidx_z = random.randint(0, len(self.link_sizes_z[idx_z]) - 1)
                self.link_sizes_z[idx_z][subidx_z] = [random.uniform(0.2, 1.2), random.uniform(0.2, 0.5),
                                                      random.uniform(0.2, 0.5)]

        # randomly select an index within the bounds of the array

    def Set_ID(self, id):
        self.myID = id