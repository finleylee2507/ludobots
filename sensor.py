import numpy

import constants
from pyrosim import pyrosim


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(constants.simulationSteps)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        with open('./data/'+self.linkName+'-sensor-values.npy', 'wb') as f:
            numpy.save(f, self.values)

