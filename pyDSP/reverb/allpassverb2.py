from ..filters.IIR.apf import *
from ..audioUnit import *
from ..delay import *

class AllPassVerb2(AudioUnit):
    def __init__(self,samplerate, initialDelaySamples, initialFeedback) -> None:
        super().__init__(samplerate)
        self.delayTime = initialDelaySamples
        self.feedback = initialFeedback
        self.filters = [
            APF(samplerate,initialFeedback,round(initialDelaySamples)+1),
            APF(samplerate,initialFeedback,round(initialDelaySamples*0.7)+1),
            APF(samplerate,initialFeedback,round(initialDelaySamples*0.6)+1),
            APF(samplerate,initialFeedback,round(initialDelaySamples*0.3)+1),
            DelayLine(samplerate,initialFeedback*0.4,initialDelaySamples/(samplerate/1000)),
            APF(samplerate,initialFeedback,round(initialDelaySamples*0.7)+1),
            APF(samplerate,initialFeedback,round(initialDelaySamples*0.3)+1)
            ]

    def readSample(self,sample):
        output = 0
        for index,filter in enumerate(self.filters):
            if index == 0:
                sample = filter.readSample(sample)
            elif index == 4:
                filter.writeSample(sample)
                sample = filter.readSample()
            else:
                sample = filter.readSample(sample)
                output+=sample
        return sample
