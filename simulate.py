import time

import numpy
import pybullet as p
import pybullet_data

import pyrosim.pyrosim as pyrosim

# back leg config
amplitudeBackLeg = numpy.pi / 4 * 10
frequencyBackLeg = 10
phaseOffsetBackLeg = 0

# front leg config
amplitudeFrontLeg = numpy.pi / 4
frequencyFrontLeg = 10
phaseOffsetFrontLeg = 0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# add gravity
p.setGravity(0, 0, -9.8)

# set floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
# read in the world described in box.sdf
p.loadSDF("world.sdf")

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

targetAnglesBackLeg = numpy.sin(
    numpy.linspace(0, numpy.pi * 2, 1000) * frequencyBackLeg + phaseOffsetBackLeg) * amplitudeBackLeg
targetAnglesFrontLeg = numpy.sin(
    numpy.linspace(0, numpy.pi * 2, 1000) * frequencyFrontLeg + phaseOffsetFrontLeg) * amplitudeFrontLeg
# with open('./data/targetAngles.npy', 'wb') as f:
#     numpy.save(f, targetAngles)


with open('./data/targetAnglesBackLeg.npy', 'wb') as f:
    numpy.save(f, targetAnglesBackLeg)

with open('./data/targetAnglesFrontLeg.npy', 'wb') as f:
    numpy.save(f, targetAnglesFrontLeg)

pyrosim.Prepare_To_Simulate(robotId)

# exit()
for i in range(1000):
    time.sleep(1 / 240)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # backleg motor
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b'Torso_BackLeg',

        controlMode=p.POSITION_CONTROL,

        targetPosition=targetAnglesBackLeg[i],

        maxForce=10)

    # frontleg motor
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b'Torso_FrontLeg',

        controlMode=p.POSITION_CONTROL,

        targetPosition=targetAnglesFrontLeg[i],

        maxForce=10)

# # save value to ./data
# with open('./data/backLegSensorValues.npy', 'wb') as f:
#     numpy.save(f, backLegSensorValues)
#
# with open('./data/frontLegSensorValues.npy', 'wb') as f:
#     numpy.save(f, frontLegSensorValues)
#
# with open('./data/targetAngles.npy', 'wb') as f:
#     numpy.save(f, targetAngles)

p.disconnect()
