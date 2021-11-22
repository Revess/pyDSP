import pyaudio
import numpy as np
import threading as td
from pyDSP.oscillator.waveforms import Sine
from pyDSP.pitchShifter import PitchShifter
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

class AudioProcessor:
    #Order matters in using the dict
    def __init__(self,samplerate=44100,channels=1,audioUnits=list(),anim = False) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits
        self.anim = anim

    def processor(self,i=0):
        if not self.anim:
            while True:
                buffer = [0] * (self.bufferSize*4)
                for i in range(self.bufferSize):
                    self.audioUnits[1].writeSample(self.audioUnits[0].get_sample())
                    buffer[i] += self.audioUnits[1].readSample()*0.75

                self.stream.write(np.array(buffer).astype(np.float32))
        else:
            bufferA = [0] * (self.bufferSize*4)
            bufferB = [0] * (self.bufferSize*4)
            for i in range(self.bufferSize):
                bufferA[i] = self.audioUnits[0].get_sample()
                self.audioUnits[1].writeSample(bufferA[i])
                bufferB[i] = self.audioUnits[1].readSample()


            plt.cla()
            plt.plot(bufferA[:self.bufferSize])
            plt.plot(bufferB[:self.bufferSize])
            plt.tight_layout()


    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

if __name__ == "__main__":
    processor = AudioProcessor(audioUnits=[Sine(220,44100,phase=0),PitchShifter()],anim=True)
    # audioThread = td.Thread(target=processor.processor,daemon=True)
    # audioThread.start()
    # try:
    #     while audioThread.is_alive():
    #         audioThread.join(1)
    # except KeyboardInterrupt:
    #     exit()
    ani = FuncAnimation(plt.gcf(),processor.processor,interval=25)
    plt.tight_layout()
    plt.show()
