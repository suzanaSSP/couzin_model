import numpy as np

class Agent:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.c = np.array([x,y])
        
