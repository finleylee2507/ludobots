# ludobots

## Running my code
To run the code, simply run 'simulate_for_assignment_7.py'. 

## Description of how bodies and brains are generated 
The first step in the program involves determining the total number of blocks that make up the body, followed by a series of coin flips to ascertain whether each block will contain a sensor or not. Then, the body is created by putting together blocks one after the other. For every block, a random shape is formed, with the side lengths chosen from a random range of 0.2 to 1. A further random number is generated to determine the next block's placement in relation to the previous one, whether in the +x, -x, +y, or -y direction. The code also randomly decides if the new block should be placed on the same level as the previous block or be elevated to the next level. To prevent the blocks from generating within each other, I created a method to check if the next direction is the opposite of the direction we just came from.Subsequently, a neural network is created by adding a sensor neuron for each block that is equipped with a sensor. Motor neurons are then attached to every link. Lastly, I loop through every motor neuron and connect it to all the sensor neurons, thus completing the construction of the brain. 

## Video: 
https://youtube.com/shorts/agWQ7bNAbu0?feature=share 

## Resources
https://www.reddit.com/r/ludobots/ 
https://www.thunderheadeng.com/pyrosim 

