import numpy as np

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