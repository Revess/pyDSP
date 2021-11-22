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
        sendData(["removeNode", focussedBox]);
        focussedBox = null;
    }
}

function addCard(object) {
    let newNode = document.createElement("div");
    newNode.id = object + cardNum;
    newNode.classList = "col-md-4 mt-5 mb-5";
    document.getElementById("cardHolder").appendChild(newNode)
    $("#" + object + cardNum).load("../blocks/" + object + ".html", function () {
        let thisObject = document.getElementById(object + cardNum)
        let allCards = document.querySelectorAll(".project-box")
        allCards.forEach((element, i) => {
            if (!element.parentElement.id.includes(object + cardNum)) {
                let outputs = element.querySelectorAll(".output")[0].children[0].children[1];
                let newNode = document.createElement("a");
                newNode.classList = "dropdown-item";
                newNode.onclick = function () { changeOutput(this) };
                newNode.innerHTML = object + cardNum;
                outputs.appendChild(newNode);
                newNode = document.createElement("a");
                newNode.classList = "dropdown-item";
                newNode.onclick = function () { changeOutput(this) };
                newNode.innerHTML = element.parentElement.id;
                thisObject.querySelectorAll(".output")[0].children[0].children[1].appendChild(newNode)
            }
        });
        document.getElementById(object + cardNum).children[0].children[0].children[0].children[0].innerHTML = newNode.children[0].children[0].children[0].children[0].innerHTML + cardNum;
        if (object.includes("Oscillator")) {
            sendData(["newNode", newNode.id, "oscillator sine"]);
        } else if (object.includes("Modulator")) {
            sendData(["newNode", newNode.id, "modulator"]);
        }
        cardNum += 1;
    });
}