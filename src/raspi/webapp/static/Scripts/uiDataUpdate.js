//NOTE!: Load main.js first!

//Helper for API get method
function apiGet(callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function(e) {
        try {
            var data = JSON.parse(xmlhttp.responseText);
        } catch (err) {
            console.log(err.message + " in " + xmlhttp.responseText);
            return;
        }
        callback(data);
    };
    xmlhttp.onerror= function(e) {
        setToDefaultValues();
    };
    xmlhttp.open("GET", '/api', true);
    xmlhttp.send();
}

// UpdateUI method (called by setInterval each 250ms)
function updateUI(data) {
    console.log("Received Data:");
    console.log(data);

    updateSoulTrainData(data);
    updateHeartBeats(data);
}

// Update logic of certain buttons depending on the data

let crane_state = "undefined";

function updateLogic(data) {

    //Update Crane buttons depending on the data (allow on only if state is 0)
    let craneOnButton = document.getElementById('craneOn');
    let craneResetButton = document.getElementById('craneReset');

    if(data != null && crane_state !== data.crane) {
        if(data.crane === "0") {
            craneOnButton.disabled = false;
            craneResetButton.disabled = true;
        } else {
            craneOnButton.disabled = true;
            craneResetButton.disabled = false;
        }

        crane_state = data.crane;
    }
}

// Update SoulTrain data received from the backend
function updateSoulTrainData(data) {
    document.getElementById("phase").innerText = data == null ? "-" : data.phase;
    document.getElementById("phaseMessage").innerText = data == null ? "-" : data.phaseMessage;
    document.getElementById("speed").innerText = data == null ? "-" : data.speed;
    document.getElementById("distance").innerText = data == null ? "-" : data.distance;
    document.getElementById("xAcceleration").innerText = data == null ? "-" : data.xAcceleration;
    document.getElementById("yAcceleration").innerText = data == null ? "-" : data.yAcceleration;
    document.getElementById("zAcceleration").innerText = data == null ? "-" : data.zAcceleration;
    document.getElementById("direction").innerText = data == null ? "-" : data.direction;
    document.getElementById("number").innerText = data == null ? "-" : data.number;
    document.getElementById("round").innerText = data == null ? "-" : data.round;
    document.getElementById("cube").innerText = data == null ? "-" : data.cube;
    document.getElementById("crane").innerText = data == null ? "-" : data.crane;

    updateLogic(data);
}

// Update the classes to display HearBeat status
function updateHeartBeats(data) {
    lineDetectorDiv = document.getElementById("lineDetectorDiv");
    numberDetectorDiv = document.getElementById("numberDetectorDiv");
    movementDiv = document.getElementById("movementDiv");
    acousticDiv = document.getElementById("acousticDiv");
    controlFlowDiv = document.getElementById("controlflowDiv");

    elements = [lineDetectorDiv, numberDetectorDiv, movementDiv, acousticDiv, controlFlowDiv];

    elements.forEach((item, index) => {
        if(item == null) {
            console.warn("Item " + index + " is null! cannot remove classes!")
        } else {
            item.classList.remove("starting", "running", "error", "finished");
        }
    });

    lineDetectorDiv.classList.add(data == null ? "error" : data.heartBeatLineDetector);
    numberDetectorDiv.classList.add(data == null ? "error" : data.heartBeatNumberDetector);
    movementDiv.classList.add(data == null ? "error" : data.heartBeatMovement);
    acousticDiv.classList.add(data == null ? "error" : data.heartBeatAcoustic);
    controlFlowDiv.classList.add(data == null ? "error" : data.heartBeatControlFlow);
}

// set to default values
function setToDefaultValues() {
    updateHeartBeats(null);
    updateSoulTrainData(null);
}

// Starting interval (all 250ms)
setInterval(function(){
    apiGet(updateUI);
}, updateInterval);
