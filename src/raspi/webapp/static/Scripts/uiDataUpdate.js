//Variables & Constants
var updateInterval = 250; // 250ms

//Helper for API get method
function apiGet(callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch (err) {
                console.log(err.message + " in " + xmlhttp.responseText);
                return;
            }
            callback(data);
        }
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

    if(crane_state !== data.crane) {
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
    document.getElementById("state").innerText = data.state;
    document.getElementById("stateMessage").innerText = data.stateMessage;
    document.getElementById("speed").innerText = data.speed;
    document.getElementById("distance").innerText = data.distance;
    document.getElementById("xAcceleration").innerText = data.xAcceleration;
    document.getElementById("yAcceleration").innerText = data.yAcceleration;
    document.getElementById("zAcceleration").innerText = data.zAcceleration;
    document.getElementById("direction").innerText = data.direction;
    document.getElementById("number").innerText = data.number;
    document.getElementById("cube").innerText = data.cube;
    document.getElementById("crane").innerText = data.crane;

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

    lineDetectorDiv.classList.add(data.heartBeatLineDetector);
    numberDetectorDiv.classList.add(data.heartBeatNumberDetector);
    movementDiv.classList.add(data.heartBeatMovement);
    acousticDiv.classList.add(data.heartBeatAcoustic);
    controlFlowDiv.classList.add(data.heartBeatControlFlow);
}

// Starting interval (all 250ms)
setInterval(function(){
    apiGet(updateUI);
}, updateInterval);
