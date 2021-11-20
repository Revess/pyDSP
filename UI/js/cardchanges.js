var cardNum = 0;
var focussedBox = null;

function focusBox(element) {
    element.classList.add("project-box-focus");
    if (focussedBox !== null) {
        document.getElementById(focussedBox).firstChild.classList.remove("project-box-focus");
    }
    focussedBox = element.parentElement.id;
}

function removeObject() {
    if (focussedBox !== null) {
        document.getElementById("cardHolder").removeChild(document.getElementById(focussedBox));
        // removeFromOutputList(focussedBox)
        sendData(["removeNode", focussedBox]);
        focussedBox = null;
    }
}

async function addCard(object) {
    let newNode = document.createElement("div");
    let audioType = "";
    newNode.id = object + cardNum;
    newNode.classList = "col-md-4 mt-5 mb-5";
    document.getElementById("cardHolder").appendChild(newNode)
    $("#" + object + cardNum).load("../blocks/" + object + ".html", function () {
        allCards = document.querySelectorAll(".project-box")
        allCards.forEach((outerElement, i) => {
            allCards.forEach((innerElement, j) => {
                let outputElements = outerElement.querySelectorAll(".output")[0].children[0].children[1].children;
                let found = false;
                for (k = 0; k < outputElements.length; k++) {
                    if (outputElements[k].innerHTML == innerElement.parentElement.id) {
                        found = true;
                    }
                }
                if (i !== j && !found) {
                    let newItem = document.createElement("a");
                    newItem.classList = "dropdown-item";
                    newItem.onclick = function () { changeOutput(this) };
                    newItem.innerHTML = innerElement.parentElement.id;
                    outerElement.querySelectorAll(".output")[0].children[0].children[1].appendChild(newItem);
                }
            });
        });
    });
    if (object.includes("Oscillator")) {
        sendData(["newNode", newNode.id, "oscillator sine"]);
    } else if (object.includes("Modulator")) {
        sendData(["newNode", newNode.id, "modulator"]);
    }
    cardNum += 1;
}