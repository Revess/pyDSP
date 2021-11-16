import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sine import Sine
from saw import Saw
from triangle import Triangle

class AudioProcessor:
    #Order matters in using the dict
    def __init__(self,samplerate=44100,channels=1,audioUnits=list()) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits

    def processor(self,i):
        #whilefunc(), while True:
        while True:
            buffer = [0] * (self.bufferSize*4)
            for i in range(self.bufferSize):
                for audioUnit in self.audioUnits:
                    buffer[i] += audioUnit.get_sample()*0.3

            self.stream.write(np.array(buffer).astype(np.float32))
        plt.cla()
        plt.plot(buffer[:self.bufferSize])
        plt.tight_layout()

    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()
    
if __name__ == "__main__":
    # processor = AudioProcessor(audioUnits=[Triangle(440,44100,0.5)])
    # processor.processor(1)
    # ani = FuncAnimation(plt.gcf(),processor.processor,interval=25)
    # plt.tight_layout()
    # plt.show()
    pass