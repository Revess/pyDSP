from math import pi,sin,cos,sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Q = 1.5
FFREQ = 100
GAIN = 1.2
SAMPLERATE = 44100

NSAMPS = 1000
SFREQ = 100
STEP = SFREQ/SAMPLERATE

A = pow(10,GAIN)
OMEGA = 2*pi*FFREQ/SAMPLERATE
SN = sin(OMEGA)
CS = cos(OMEGA)
ALPHA = SN / (2*Q)
BETA = sqrt(A+A)
delayLine = [0] * 4

##Load coefficients
#Lowpass
a0 = 1 + ALPHA
b0 = ((1-CS) / 2)/a0
coefficients = [(1 - CS)/a0,((1-CS) / 2)/a0,(-2 * CS)/a0,(1 - ALPHA)/a0]

##Start generateting
phase = 0
saw = list()
filtered = list()

def animate(i):
    global phase,filtered,saw,coefficients,b0,a0,delayLine,BETA,ALPHA,CS,SN,A,OMEGA,STEP,SFREQ,NSAMPS,SAMPLERATE,GAIN,FFREQ,Q
    if phase >= 1:
        phase -= 1
    sample = (phase*2)-1
    phase += STEP
    saw.append(sample)
    output = (b0*sample) + (delayLine[0] * coefficients[0]) + (delayLine[1] * coefficients[1]) - (delayLine[2] * coefficients[2]) - (delayLine[3] * coefficients[3])
    delayLine[1] = delayLine[0]
    delayLine[0] = sample
    delayLine[3] = delayLine[2]
    delayLine[2] = output
    filtered.append(output)
    plt.cla()
    plt.plot(delayLine)

ani = animation.FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()

plt.plot(saw)
plt.plot(filtered)
plt.show()