import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#add gravity
p.setGravity(0,0,-9.8)

#set floor
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
#read in the world described in box.sdf
p.loadSDF("world.sdf")
for i in range(1000000):
    print(i)
    time.sleep(1/60)
    p.stepSimulation()
p.disconnect()
