from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import sys
import random
# for i in range(0, 5):
#     os.system("python generate.py")
#     os.system("python simulate.py")

#set up
if len(sys.argv) == 2:
    random.seed(int(sys.argv[1]))
    c.seed = int(sys.argv[1])
else:
    c.seed = random.randint(1, 10000)
    random.seed(c.seed)

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()

input("Press Enter to Continue")
phc.Show_Best()


