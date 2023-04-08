import random 

# define a random agent for discrete action space
class RandomDiscreteAgent(object):
    def __init__(self, n):
        self.n = n

    def act(self):
        return random.randint(0, self.n-1)

# define a random agent for continuous action space

# define a MPC agent for discrete action space

# define a MPC agent for continuous action space

# define a DQN agent for discrete action space

# define a DQN agent for continuous action space