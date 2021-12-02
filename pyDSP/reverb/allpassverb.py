from ..filters.IIR.apf import *
from ..audioUnit import *

class AllPassVerb(AudioUnit):
    def __init__(self,samplerate, initialDelaySamples, initialFeedback, numDelays = 1, delayRatios = [], feedbackRatios = []) -> None:
        super().__init__(samplerate)
        self.delayTime = initialDelaySamples
        self.feedback = initialFeedback
        self.filters = list()
        assert(len(delayRatios) == numDelays)
        assert(len(feedbackRatios) == numDelays)
        for i in range(numDelays):
            self.filters.append(APF(samplerate,initialFeedback*feedbackRatios[i],round(initialDelaySamples*delayRatios[i])+1))

    def readSample(self,sample):
        for filter in self.filters:
            sample = filter.readSample(sample)
        return sample
