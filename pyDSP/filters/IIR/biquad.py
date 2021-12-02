from ...audioUnit import AudioUnit
from math import sin,cos,sqrt,pi


class Biquad(AudioUnit):
    def __init__(self,type,cutoff,q,gain,samplerate) -> None:
        super().__init__(samplerate)
        self.type = type
        self.cutoff = cutoff
        self.q = q
        self.gain = gain

        #Variables for calculating biquad coefficients
        self.a = pow(10,self.gain)
        self.omega = 2*pi*self.cutoff/self.samplerate
        self.sn = sin(self.omega)
        self.cs = cos(self.omega)
        self.alpha = self.sn / (2*self.q)
        self.beta = sqrt(self.a+self.a)

        self.buffer = [0] * 4
        self.aCoefficients = [0] * 3
        self.bCoefficients = [0] * 3
        self.Z1 = 0
        self.Z2 = 0
        self.setCoefficients()

    def readSample(self,sample):
        output = (sample*self.bCoefficients[0])+self.Z1
        self.Z1 = (sample*self.bCoefficients[1])+self.Z2-(output*self.aCoefficients[1])
        self.Z2 = (sample*self.bCoefficients[2])-(output*self.aCoefficients[2])
        return output
        #DFI
        '''
        output = (self.bCoefficients[0]*sample) + (self.bCoefficients[1]*self.buffer[0]) + (self.bCoefficients[2]*self.buffer[1]) - (self.aCoefficients[1]*self.buffer[2]) - (self.aCoefficients[2]*self.buffer[3])
        self.buffer[3] = self.buffer[2]
        self.buffer[2] = output
        self.buffer[1] = self.buffer[0]
        self.buffer[0] = sample
        return output
        '''

    def setFilterProperties(self,type=None,cutoff=None,q=None,gain=None):
        print(type,cutoff,q,gain)
        if type is not None:
            self.type = type
        elif cutoff is not None:
            self.cutoff = cutoff
        elif q is not None:
            self.q = q
        elif gain is not None:
            self.gain = gain
        if type is not None or cutoff is not None or q is not None or gain is not None:
            self.a = pow(10,self.gain)
            self.omega = 2*pi*self.cutoff/self.samplerate
            self.sn = sin(self.omega)
            self.cs = cos(self.omega)
            self.alpha = self.sn / (2*self.q)
            self.beta = sqrt(self.a+self.a)
            self.setCoefficients()

    def setCoefficients(self):
        if self.type == "LPF":
            self.aCoefficients[0] = 1+self.alpha
            self.aCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.aCoefficients[2] = (1-self.alpha)/self.aCoefficients[0]
            self.bCoefficients[0] = ((1-self.cs)/2)/self.aCoefficients[0]
            self.bCoefficients[1] = (1-self.cs)/self.aCoefficients[0]
            self.bCoefficients[2] = ((1-self.cs)/2)/self.aCoefficients[0]
        elif self.type == "HPF":
            self.aCoefficients[0] = 1+self.alpha
            self.aCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.aCoefficients[2] = (1-self.alpha)/self.aCoefficients[0]
            self.bCoefficients[0] = ((1+self.cs)/2)/self.aCoefficients[0]
            self.bCoefficients[1] = (-(1+self.cs))/self.aCoefficients[0]
            self.bCoefficients[2] = ((1+self.cs)/2)/self.aCoefficients[0]
        elif self.type == "BP":
            self.aCoefficients[0] = 1+self.alpha
            self.aCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.aCoefficients[2] = (1-self.alpha)/self.aCoefficients[0]
            self.bCoefficients[0] = self.alpha/self.aCoefficients[0]
            self.bCoefficients[1] = 0/self.aCoefficients[0]
            self.bCoefficients[2] = (-(self.alpha))/self.aCoefficients[0]
        elif self.type == "N":
            self.aCoefficients[0] = 1+self.alpha
            self.aCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.aCoefficients[2] = (1-self.alpha)/self.aCoefficients[0]
            self.bCoefficients[0] = 1/self.aCoefficients[0]
            self.bCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.bCoefficients[2] = 1/self.aCoefficients[0]
        elif self.type == "P":
            self.aCoefficients[0] = 1+(self.alpha/self.a)
            self.aCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.aCoefficients[2] = (1-(self.alpha/self.a))/self.aCoefficients[0]
            self.bCoefficients[0] = (1+(self.alpha*self.a))/self.aCoefficients[0]
            self.bCoefficients[1] = (-2*self.cs)/self.aCoefficients[0]
            self.bCoefficients[2] = (1-(self.alpha*self.a))/self.aCoefficients[0]
        elif self.type == "LS":
            self.aCoefficients[0] = (self.a+1)+(self.a-1)*self.cs+self.beta*self.sn
            self.aCoefficients[1] = (-2*((self.a-1)+(self.a+1)*self.cs))/self.aCoefficients[0]
            self.aCoefficients[2] = ((self.a+1)+(self.a-1)*self.cs-self.beta*self.sn)/self.aCoefficients[0]
            self.bCoefficients[0] = (self.a*((self.a+1)-(self.a-1)*self.cs+self.beta*self.sn))/self.aCoefficients[0]
            self.bCoefficients[1] = (2*self.a*((self.a-1)-(self.a+1)*self.cs))/self.aCoefficients[0]
            self.bCoefficients[2] = (self.a*((self.a+1)-(self.a-1)*self.cs-self.beta*self.sn))/self.aCoefficients[0]
        elif self.type == "HS":
            self.aCoefficients[0] = (self.a+1)-(self.a-1)*self.cs+self.beta*self.sn
            self.aCoefficients[1] = (2*((self.a+1)-(self.a-1)*self.cs))/self.aCoefficients[0]
            self.aCoefficients[2] = ((self.a+1)-(self.a-1)*self.cs-self.beta*self.sn)/self.aCoefficients[0]
            self.bCoefficients[0] = (self.a*((self.a+1)+(self.a-1)*self.cs+self.beta*self.sn))/self.aCoefficients[0]
            self.bCoefficients[1] = (-2*self.a*((self.a-1)-(self.a+1)*self.cs))/self.aCoefficients[0]
            self.bCoefficients[2] = (self.a*((self.a+1)-(self.a-1)*self.cs-self.beta*self.sn))/self.aCoefficients[0]