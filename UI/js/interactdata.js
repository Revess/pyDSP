function findName(object, breaker) {
    var name = "";
    let parent = object;
    while (name.length == 0) {
        id = parent.parentElement.id.toString()
        if (id.includes(breaker)) {
            name = id;
        }
        parent = parent.parentElement;
    }
    return name
}

function frequencyChange(object) {
    sendData(["oscFrequency", findName(object, "Oscillator"), object.value])
}

function volumeChange(object) {
    sendData(["oscVolume", findName(object, "Oscillator"), object.value])
}

function angleChange(object) {
    sendData(["oscAngle", findName(object, "Oscillator"), object.value])
}

function changeWaveForm(object) {
    if (object.innerHTML == "Triangle" || object.innerHTML == "Square") {
        object.parentElement.parentElement.parentElement.parentElement.querySelector(".angle-slider").classList.remove("hidden-element")
    } else {
        object.parentElement.parentElement.parentElement.parentElement.querySelector(".angle-slider").classList.add("hidden-element")
    }
    object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    sendData(["oscWave", findName(object, "Oscillator"), "oscillator " + object.innerHTML])
}

function voiceChange(object) {
    sendData(["oscVoice", findName(object, "Oscillator"), object.value])
}

function detuneChange(object) {
    sendData(["oscDetune", findName(object, "Oscillator"), object.value])
}

function sendData(data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: data
    }));
}