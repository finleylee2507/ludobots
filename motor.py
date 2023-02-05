import numpy
import pybullet as p

from pyrosim import pyrosim

import numpy

class MOTOR:
    def __init__(self, jointName, amplitude, frequency, offset):
        self.jointName = jointName
        self.values = numpy.zeros(1000)
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset = offset

        self.targetAngles = numpy.linspace(0, numpy.pi * 2, 1000)
        for i in range(1000):
            self.values[i] = self.amplitude * numpy.sin(self.frequency * self.targetAngles[i] + self.offset)

    def Set_Value(self, robot,desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot, jointName=self.jointName, controlMode=p.POSITION_CONTROL,
                                    targetPosition=desiredAngle, maxForce=1000)
