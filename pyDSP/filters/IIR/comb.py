from ...delay import DelayLine

class IIRComb(DelayLine):
    def __init__(self,samplerate,feedback,lengthInSamples=None,lengthInMS=None) -> None:
        super().__init__(samplerate,feedback,lengthInSamples,lengthInMS)