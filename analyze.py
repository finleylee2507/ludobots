import numpy
import matplotlib.pyplot

with open('./data/backLegSensorValues.npy', 'rb') as f:
    backLegSensorValues = numpy.load(f)


with open('./data/frontLegSensorValues.npy', 'rb') as f:
    frontLegSensorValues = numpy.load(f)

# print(backLegSensorValues)
# print(frontLegSensorValues)

matplotlib.pyplot.plot(backLegSensorValues,label="back leg sensor",linewidth=2)
matplotlib.pyplot.plot(frontLegSensorValues,label="front leg sensor",linewidth=2)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()