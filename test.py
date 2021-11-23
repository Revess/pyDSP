import matplotlib.pyplot as plt
from math import pi,cos,sin,fmod
from random import random

x = range(1000)
output = [0]*len(x)
phase = 0
step = 220/44100
for i in x:
    if phase >= 1:
        phase -= 1
    sample = (phase*2)-1
    output[i] = output[i-1]-(0.5*(output[i-1]-sample))
    phase+=step

plt.plot(range(len(output)),output)
plt.show()