import matplotlib.pyplot as plt
from math import pi,cos,sin,ceil,fmod

speed = 1/(1-0.5)
delayLength = 1
while round(fmod(delayLength,speed),2) != 0.0:
    delayLength+=1
    if delayLength >= 20 and round(fmod(delayLength,speed),2) < 0.5:
        break

x = range(1000)
sine = list()
stretched = [0] * delayLength
delay = [0] * delayLength
writeHead = 0
output = list()
phase = 0
step = 220/44100
for i in x:
    if phase >= 1:
        phase-=1
    sample = sin(phase*(2*pi))
    for i in range(delayLength):
        delay[(writeHead+i)%delayLength] = sample+(delay[(writeHead+i)%delayLength]* (((delayLength-1)-i)/(delayLength-1)))
        output.append((delay[(writeHead+i)%delayLength]/16)-1)
    writeHead+=1
    writeHead%=delayLength
    sine.append(sample)
    phase+=step

plt.plot(range(len(sine)),sine)
plt.plot(range(len(output)),output)
plt.show()