from ...audioUnit import AudioUnit
from .biquad import Biquad

class IIRMultiFilter(AudioUnit):
    def __init__(self,samplerate,filters={"LPF1":["LPF",220,1,1]}) -> None:
        super().__init__(samplerate)
        self.filters = dict()
        for filterName,properties in filters.items():
            self.filters.update({filterName:Biquad(properties[0],properties[1],properties[2],properties[3],samplerate)})

    def readSample(self,sample):
        output = 0
        for filterName,filter in self.filters.items():
            output += filter.readSample(sample)
        return output/len(self.filters)

    def setFilterProperties(self,filters,type=None,cutoff=None,q=None,gain=None):
        for filter in filters:
            self.filters[filter].setFilterProperties(type=None,cutoff=None,q=None,gain=None)

    def getFilterNames(self):
        return self.filters.keys()
