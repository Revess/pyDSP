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

function checkOutputList() {
    allCards = document.querySelectorAll(".project-box")
    allCards.forEach((outerElement, i) => {
        allCards.forEach((innerElement, j) => {
            console.log(outerElement, innerElement);
            // let outputElements = e.querySelectorAll(".output")[0].children[0].children[1].children;
            // let found = false;
            // for (k = 0; k < outputElements.length; k++) {
            //     if (outputElements[k].innerHTML == el.parentElement.id) {
            //         found = true;
            //     }
            // }
            // if (i !== j && !found) {
            //     let newItem = document.createElement("a");
            //     newItem.classList = "dropdown-item";
            //     newItem.onclick = function () { changeOutput(this) };
            //     newItem.innerHTML = el.parentElement.id;
            //     e.querySelectorAll(".output")[0].children[0].children[1].appendChild(newItem);
            // }
            // if (i !== j) {
            //     inputs = [".FM-slider", ".AM-slider", ".RM-slider"]
            //     inputs.forEach(element => {
            //         inputList = document.getElementById(el.parentElement.id).querySelectorAll(element)[0].children[0].children[0].children
            //         for (k = 0; k < inputList[1].children.length; k++) {
            //             if (inputList[1].children[k].innerHTML == e.parentElement.id) {
            //                 inputList[0].innerHTML = element.replace(".", "").replace("-slider", "")
            //                 inputList[1].removeChild(inputList[1].children[k])
            //             }
            //         }
            //     });
            // }
        });
    });
}

function removeFromOutputList(object) {
    allCards = document.querySelectorAll(".output")
    allCards.forEach(element => {
        EChilds = element.children[0].children[1].children
        for (i = 0; i < EChilds.length; i++) {
            if (EChilds[i].innerHTML == object) {
                element.children[0].children[1].removeChild(EChilds[i])
            }
        }
    });
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
    let previousTarget = object.parentElement.parentElement.children[0].innerText
    if (!previousTarget.includes("Direct Out")) {
        if (object.innerText == "Direct Out" || object.innerText !== previousTarget) {
            console.log(previousTarget)
            targetElement = document.getElementById(previousTarget).querySelectorAll(".output")[0].children[0].children[1].removeChild(object)
        }
    }

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

    sendData(["oscOutput", findName(object, "Oscillator"), object.innerHTML])
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