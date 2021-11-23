import pyaudio
import numpy as np
import threading as td
from pyDSP.waves.waveforms import *
from pyDSP.filters.lowPass import LowPass
import matplotlib.pyplot as plt
import os
import scipy.fftpack

SAMPLERATE = 44100

class AudioProcessor:
    def __init__(self,samplerate=44100,channels=1,audioUnits=list(),drawOutput = True) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits
        self.drawOutput = drawOutput 

    def processor(self,i=0):
        digitalImage = list()
        while True:
            buffer = [0] * (self.bufferSize*4)
            for i in range(self.bufferSize):
                buffer[i] += self.audioUnits[1].get_sample(self.audioUnits[0].get_sample())

                if self.drawOutput:
                    digitalImage.append(buffer[i])

            self.stream.write(np.array(buffer).astype(np.float32))

            if len(digitalImage) >= 1024 and self.drawOutput:
                plt.plot(range(len(digitalImage)),digitalImage)
                plt.tight_layout
                plt.savefig("./plots/"+str(len(os.listdir("./plots"))+1)+".png",format="png")
                plt.clf()
                y = np.fft.fft(digitalImage)
                freq = (np.fft.fftfreq(len(y))[1:len(y)//2]*22050)[20:5000]
                y = abs(y[1:len(y)//2])[20:5000]
                y/=np.max(y)
                plt.plot(freq,y)
                plt.ylim(0,np.max(y))
                plt.savefig("./fft/"+str(len(os.listdir("./fft"))+1)+".png",format="png")
                plt.clf()
                digitalImage = list()

    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

def commands():
    while True:
        Lp.setCutoff(int(input(">>")))

def emptyPlots():
    files = os.listdir("./plots/")
    for f in files:
        os.remove("./plots/"+f)
    files = os.listdir("./fft/")
    for f in files:
        os.remove("./fft/"+f)

if __name__ == "__main__":
    emptyPlots()
    Lp = LowPass(4000,44100)
    processor = AudioProcessor(audioUnits=[Saw(440,SAMPLERATE),Lp],drawOutput=True)
    audioThread = td.Thread(target=processor.processor,daemon=True)
    commandLine = td.Thread(target=commands,daemon=True)
    plt.tight_layout()
    audioThread.start()
    commandLine.start()
    try:
        while audioThread.is_alive():
            audioThread.join(1)
            commandLine.join(1)
    except KeyboardInterrupt:
        exit()