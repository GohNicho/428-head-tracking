import numpy as np
import time
from analyzer import *

def gen_data(t):
    # generates mock data to test the analyzer
    # input - t (time)
    # output - sinusoidal value to simulate data
    
    return np.sin(t) * np.cos(2*t)


def gen_data(t):
    # generate realtime data
    
    t = 0
    
    while t < 150:
        print(gen_data(t))
        t += 1
        
########### Simulation code here ##############
        
def test_analyzer():
    system = HTSystem()
    system.add_client("Vera", "Sipicki")
    
    i = 0
    t = time.time()
    
    while i < 10000000:
        if i % 2 == 0 and time.time()-t > 5.1:
            system.read([i+0.01, i+0.02, i+0.03], "left")
            print ("sent left")
        elif i % 2 == 1 and time.time()-t > 5:
            system.read([i+0.01, i+0.02, i+0.03], "None")
            print ("sent none")
        i += 1
    print ("done")
    system.get_choices_tree()
    
if __name__ == "__main__":
    test_analyzer()