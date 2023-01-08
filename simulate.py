import pybullet as p
import time

physicsClient = p.connect(p.GUI)

#read in the world described in box.sdf
p.loadSDF("box.sdf")
for i in range(1000):
    print(i)
    time.sleep(1/60)
    p.stepSimulation()
p.disconnect()
