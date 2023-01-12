import time

import numpy
import pybullet as p
import pybullet_data

import pyrosim.pyrosim as pyrosim

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# add gravity
p.setGravity(0, 0, -9.8)

# set floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
# read in the world described in box.sdf
p.loadSDF("world.sdf")

backLegSensorValues = numpy.zeros(100)
frontLegSensorValues = numpy.zeros(100)

pyrosim.Prepare_To_Simulate(robotId)
for i in range(100):
    time.sleep(1 / 60000)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

print(backLegSensorValues)

# save value to ./data
with open('./data/backLegSensorValues.npy', 'wb') as f:
    numpy.save(f, backLegSensorValues)

with open('./data/frontLegSensorValues.npy', 'wb') as f:
    numpy.save(f, frontLegSensorValues)

p.disconnect()
