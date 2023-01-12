import matplotlib.pyplot
import numpy

with open('./data/backLegSensorValues.npy', 'rb') as f:
    backLegSensorValues = numpy.load(f)

with open('./data/frontLegSensorValues.npy', 'rb') as f:
    frontLegSensorValues = numpy.load(f)

with open('./data/targetAnglesBackLeg.npy', 'rb') as f:
    targetAnglesBackLeg = numpy.load(f)

with open('./data/targetAnglesFrontLeg.npy', 'rb') as f:
    targetAnglesFrontLeg = numpy.load(f)

# print(backLegSensorValues)
# print(frontLegSensorValues)

# matplotlib.pyplot.plot(backLegSensorValues,label="back leg sensor",linewidth=2)
# matplotlib.pyplot.plot(frontLegSensorValues,label="front leg sensor",linewidth=2)
# matplotlib.pyplot.legend()

matplotlib.pyplot.plot(targetAnglesBackLeg, label="backLeg Target Angles", linewidth=5)
matplotlib.pyplot.plot(targetAnglesFrontLeg, label="frontLeg Target Angles", linewidth=1)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
