import pyaudio
import numpy as np
import threading as td
from pyDSP.oscillator.waveforms import Sine
from pyDSP.pitchShifter import PitchShifter
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

class AudioProcessor:
    #Order matters in using the dict
    def __init__(self,samplerate=44100,channels=1,audioUnits=list()) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 128
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits

    def processor(self,i=0):
        while True:
            outbuffer = [0] * (self.bufferSize*4)
            inbuffer = np.frombuffer(self.stream.read(self.bufferSize),'float32')
            for i in range(self.bufferSize):
                self.audioUnits[0].writeSample(inbuffer[i])
                outbuffer[i] += self.audioUnits[0].readSample()*0.75
            self.stream.write(np.array(outbuffer).astype(np.float32))

    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()
        exit()

def commands():
    while True:
        pitchShifter.changePitch(float(input(">>")))

if __name__ == "__main__":
    pitchShifter = PitchShifter(20)
    processor = AudioProcessor(audioUnits=[pitchShifter])
    audioThread = td.Thread(target=processor.processor,daemon=True)
    inputThread = td.Thread(target=commands,daemon=True)
    audioThread.start()
    inputThread.start()
    try:
        while audioThread.is_alive():
            audioThread.join(1)
            inputThread.join(1)
    except KeyboardInterrupt:
        exit()