import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyDSP.synth.synth import Synth


class AudioProcessor:
    #Order matters in using the dict
    def __init__(self,samplerate=44100,channels=1,audioUnits=list()) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits

    def processor(self):
        while True:
            buffer = [0] * (self.bufferSize*4)
            for i in range(self.bufferSize):
                for audioUnit in self.audioUnits:
                    buffer[i] += audioUnit.get_sample()*(1/len(self.audioUnits))

            self.stream.write(np.array(buffer).astype(np.float32))

    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()
    
if __name__ == "__main__":
    processor = AudioProcessor(audioUnits=[Synth()])
    processor.processor()