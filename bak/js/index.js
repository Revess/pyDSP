// $(function () {
//     $("#navbar").load("../blocks/navbar.html");
// });

var oscillatorNum = 0

function addOscillator() {
    let newNode = document.createElement("div")
    newNode.id = "oscillator" + oscillatorNum
    newNode.classList = "col-md-4 mt-3 mb-3"
    document.getElementById("cardHolder").appendChild(newNode)
    $("#" + "oscillator" + oscillatorNum).load("../blocks/oscillator.html");
    oscillatorNum += 1
}

function frequencyChange(object) {
    var oscillatorName = "";
    let parent = object;
    while (oscillatorName.length == 0) {
        let id = parent.parentElement.id.toString()
        if (id.includes("oscillator")) {
            oscillatorName = id;
        }
        parent = parent.parentElement;
    }
    sendData([object.value, "frequency", oscillatorName])
}

function sendData(data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: data
    }));
}