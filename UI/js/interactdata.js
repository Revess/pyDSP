function findName(object, breaker) {
    var name = "";
    let parent = object;
    while (name.length == 0) {
        let id = parent.parentElement.id
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

function FMChange(object) {
    sendData(["oscFm", findName(object, "Oscillator"), object.value])
}

function AMChange(object) {
    sendData(["oscAm", findName(object, "Oscillator"), object.value])
}

function RMChange(object) {
    sendData(["oscRm", findName(object, "Oscillator"), object.value])
}

function changeFMInput(object) {
    object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    sendData(["oscFMInput", findName(object, "Oscillator"), object.innerHTML])
}

function changeAMInput(object) {
    object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    sendData(["oscAMInput", findName(object, "Oscillator"), object.innerHTML])
}

function changeRMInput(object) {
    object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    sendData(["oscRMInput", findName(object, "Oscillator"), object.innerHTML])
}

function changeOutput(object) {
    //If previous target is not Direct Output:
    //Remove this name from the previous target inputs
    //Add this mane to the previous target outputs

    //When choosing a target:
    //Remove this name from the target output
    //Add this name to the target inputs
    let previousTarget = object.parentElement.parentElement.children[0].innerHTML
    let objectID = findName(object, "Oscillator")
    console.log("previousTarget: " + previousTarget)
    console.log("newTarget: " + object.innerHTML)
    console.log("currentObject: " + objectID)
    if (!previousTarget.includes("Direct Out")) {
        if (object.innerHTML.includes("Direct Out") || !object.innerHTML.includes(previousTarget)) {
            targetElement = document.getElementById(previousTarget).querySelectorAll(".output")[0].children[0].children[1]
            let newNode = object.cloneNode(true)
            newNode.innerHTML = findName(object, "Oscillator")
            newNode.onclick = function () { changeOutput(this) };
            targetElement.appendChild(newNode)
        }
        if (!object.innerHTML.includes(previousTarget) && !object.innerHTML.includes("Direct Out")) {
            targetElement = document.getElementById(object.innerHTML).querySelectorAll(".output")[0].children[0].children[1]
            for (i = 0; i < targetElement.children.length; i++) {
                if (targetElement.children[i].innerHTML.includes(objectID)) {
                    targetElement.removeChild(targetElement.children[i])
                }
            }
        }
    } else {
        targetElement = document.getElementById(object.innerHTML).querySelectorAll(".output")[0].children[0].children[1]
        for (i = 0; i < targetElement.children.length; i++) {
            if (targetElement.children[i].innerHTML.includes(objectID)) {
                targetElement.removeChild(targetElement.children[i])
            }
        }
    }

    object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    sendData(["oscOutput", findName(object, "Oscillator"), object.innerHTML])
    object.innerHTML = previousTarget

    // object.parentElement.parentElement.children[0].innerHTML = object.innerHTML
    // if (object.innerHTML.includes("Direct Out")) {
    //     checkOutputList();
    // } else {
    //     removeFromOutputList(findName(object, "Oscillator"))
    //     console.log(object)
    //     inputs = [".FM-slider", ".AM-slider", ".RM-slider"]
    //     inputs.forEach(element => {
    //         inputList = document.getElementById(object.innerHTML).querySelectorAll(element)[0].children[0].children[0].children[1]
    //         inputElement = inputList.children[0].cloneNode(true);
    //         inputElement.innerHTML = findName(object, "Oscillator")
    //         inputList.appendChild(inputElement)
    //     });
    // }

}

function changeWaveForm(object) {
    if (object.innerHTML == "Triangle" || object.innerHTML == "Square") {
        object.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector(".angle-slider").classList.remove("hidden-element")
    } else {
        object.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector(".angle-slider").classList.add("hidden-element")
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