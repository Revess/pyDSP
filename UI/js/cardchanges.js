var cardNum = 0;
var focussedBox = null;

function focusBox(element) {
    element.classList.add("project-box-focus")
    if (focussedBox !== null) {
        document.getElementById(focussedBox).firstChild.classList.remove("project-box-focus")
    }
    focussedBox = element.parentElement.id
}

function removeObject() {
    if (focussedBox !== null) {
        document.getElementById("cardHolder").removeChild(document.getElementById(focussedBox))
        sendData(["removeNode", focussedBox])
        focussedBox = null;
    }
}

function addCard(object) {
    console.log(object)
    let newNode = document.createElement("div")
    let audioType = ""
    newNode.id = object + cardNum
    newNode.classList = "col-md-4 mt-5 mb-5"
    document.getElementById("cardHolder").appendChild(newNode)
    $("#" + object + cardNum).load("../blocks/" + object + ".html");
    if (object.includes("Oscillator")) {
        sendData(["newNode", newNode.id, "oscillator sine"])
    } else if (object.includes("Modulator")) {
        sendData(["newNode", newNode.id, "modulator"])
    }
    cardNum += 1
}