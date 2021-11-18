import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyDSP.oscillator.synth import Synth
from flask import Flask
from flask import request
import threading as td

app = Flask(__name__,static_url_path="",static_folder="./UI/",template_folder="./UI/")
SAMPLERATE = 44100

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        data = list(request.get_json().values())[0]
        if "newNode" in data[0]:
            processor.addAudioUnit(data[1],data[2].lower())
        elif "removeNode" in data[0]:
            processor.removeAudioUnit(data[1])
        elif "oscFrequency" in data[0]:
            processor.changeAudioUnitProperty(data[1],"frequency",data[2])
        elif "oscVolume" in data[0]:
            processor.changeAudioUnitProperty(data[1],"volume",data[2])
        elif "oscAngle" in data[0]:
            processor.changeAudioUnitProperty(data[1],"angle",data[2])
        elif "oscDetune" in data[0]:
            processor.changeAudioUnitProperty(data[1],"detune",data[2])
        elif "oscVoice" in data[0]:
            processor.changeAudioUnitProperty(data[1],"voices",data[2])
        elif "oscWave" in data[0]:
            processor.changeAudioUnitProperty(data[1],"waveform",data[2].lower())
        return "done"
    else:
        return app.send_static_file("./index.html")

class AudioProcessor:
    #Order matters in using the dict
    def __init__(self,samplerate=44100,channels=1,audioUnits=dict()) -> None:
        self.pyAudio = pyaudio.PyAudio()
        self.bufferSize = 1024
        self.stream = self.pyAudio.open(format=pyaudio.paFloat32,rate=samplerate,channels=channels,input=True,output=True,frames_per_buffer=self.bufferSize)
        self.audioUnits = audioUnits

    def processor(self):
        while True:
            buffer = [0] * (self.bufferSize*4)
            for i in range(self.bufferSize):
                for key,audioUnit in self.audioUnits.items():
                    buffer[i] += audioUnit.get_sample()*(1/len(self.audioUnits))

            self.stream.write(np.array(buffer).astype(np.float32))

    def killProcess(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

    def addAudioUnit(self,unitID,unitType):
        unit = None
        if "oscillator" in unitType:
            unit = Synth()
            self.audioUnits.update({unitID:unit})

    def removeAudioUnit(self,unitID):
        del self.audioUnits[unitID]

    def changeAudioUnitProperty(self,unitID,property,value):
        self.audioUnits[unitID].changeProperty(property,value)
    
if __name__ == "__main__":
    processor = AudioProcessor()
    audioThread = td.Thread(target=processor.processor,daemon=True)
    audioThread.start()
    try:
        app.run("127.0.0.1", 8080, True)
        while audioThread.is_alive():
            audioThread.join(1)
    except KeyboardInterrupt:
        exit()
    