from math import pi,sin,cos,sqrt,e,log10
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Q = 1
FFREQ = 5000
GAIN = 1
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

BINSIZE = 512  # number of frequency points
FSTEP = (SAMPLERATE/2) / BINSIZE  # distance between two frequency points

H = [0] * BINSIZE
for n in range(BINSIZE):
    f0 = n*FSTEP
    z = e**(2j*pi*f0/SAMPLERATE)

    num = b0 + coefficients[0]/z + coefficients[1]/z**2
    denom = a0 + coefficients[2]/z + coefficients[3]/z**2
    H[n]=abs(num/denom)

# Now just do the plotting
frange = [i*FSTEP for i in range(round((SAMPLERATE/2)/FSTEP))]
plt.plot(frange, [20*log10(h) for h in H])
plt.ylim((-30,5))
plt.grid(True)
plt.show()
exit()

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