import pyaudio
import numpy as np
from pyDSP.reverb.allpassverb2 import *
import threading as td

SAMPLERATE = 44100
BLOCKSIZE = 4048
CHANNELS = 1

class AudioProcessor:
    def __init__(self,samplerate=44100,channels=1,audioTrack=list()) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(
            format=pyaudio.paFloat32,
            rate=samplerate,
            channels=channels,
            input=True,
            output=True,
            frames_per_buffer=self.bufferSize
        )
        self.audioTrack = audioTrack

    def processor(self):
        while True:
            buffer = [0] * (self.bufferSize*4)
            inputbuffer = np.frombuffer(self.stream.read(self.bufferSize),"Float32")
            for i in range(self.bufferSize):
                for unit in self.audioTrack:
                    buffer[i] += unit.readSample(inputbuffer[i])
            self.stream.write(np.array(buffer).astype(np.float32))

def commands():
    while True:
        state = input(">>").split()
        if state[0] == "exit":
            exit()

if __name__ == "__main__":
    processor = AudioProcessor(audioTrack=[AllPassVerb2(SAMPLERATE,(SAMPLERATE/1000)*100,0.9)])
    audioThread = td.Thread(target=processor.processor,daemon=True)
    commandLine = td.Thread(target=commands,daemon=True)
    audioThread.start()
    commandLine.start()
    try:
        while audioThread.is_alive():
            audioThread.join(1)
            commandLine.join(1)
    except KeyboardInterrupt:
        exit()