import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyDSP.synth.synth import Synth
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
            processor.addAudioUnit(data[1].lower(),data[2].lower())
        elif "removeNode" in data[0]:
            processor.removeAudioUnit(data[1].lower())
        elif "oscFrequency" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"frequency",data[2].lower())
        elif "oscVolume" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"volume",data[2].lower())
        elif "oscAngle" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"angle",data[2].lower())
        elif "oscDetune" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"detune",data[2].lower())
        elif "oscVoice" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"voices",data[2].lower())
        elif "oscWave" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"waveform",data[2].lower())
        elif "oscFm" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"Fm",data[2].lower())
        elif "oscAm" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"Am",data[2].lower())
        elif "oscRm" in data[0]:
            processor.changeAudioUnitProperty(data[1].lower(),"Rm",data[2].lower())
        elif "oscFMInput" in data[0] and data[2] is not None:
            processor.changeAudioUnitProperty(data[1].lower(),"FMInput",data[2].lower())
        elif "oscAMInput" in data[0] and data[2] is not None:
            processor.changeAudioUnitProperty(data[1].lower(),"AMInput",data[2].lower())
        elif "oscRMInput" in data[0] and data[2] is not None:
            processor.changeAudioUnitProperty(data[1].lower(),"RMInput",data[2].lower())
        elif "oscOutput" in data[0]:
            processor.changeAudioUnitOutput(data[1].lower(),data[2].lower())
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

    def findAudioUnit(self,unitID):
        if unitID not in self.audioUnits.keys():
            for key in self.audioUnits.keys():
                for subKey in self.audioUnits[key].getModulators().keys():
                    if subKey == unitID:
                        return key
        else:
            return unitID

    def changeAudioUnitProperty(self,unitID,property,value):
        foundKey = self.findAudioUnit(unitID)
        if foundKey == unitID:
            self.audioUnits[unitID].changeProperty(property,value)
        else:
            self.audioUnits[foundKey].modifyModulator(unitID,property,value)

    def changeAudioUnitOutput(self,unitID,value):
        if unitID not in self.audioUnits.keys() and "direct out" in value:
            for key,audioUnit in self.audioUnits.items():
                if unitID in audioUnit.getModulators().keys():
                    self.audioUnits.update({unitID:audioUnit.getModulatorValue(unitID)})
                    audioUnit.removeInput(unitID)
                    break
        elif value in self.audioUnits.keys():
            self.audioUnits[value].addInput(unitID,self.audioUnits[unitID])
            del self.audioUnits[unitID]
    
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
    