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

// Update SoulTrain data received from the backend
function updateSoulTrainData(data) {
    document.getElementById("state").innerText = data.state;
    document.getElementById("stateMessage").innerText = data.stateMessage;
    document.getElementById("speed").innerText = data.speed;
    document.getElementById("position").innerText = data.position;
    document.getElementById("xAcceleration").innerText = data.xAcceleration;
    document.getElementById("yAcceleration").innerText = data.yAcceleration;
    document.getElementById("zAcceleration").innerText = data.zAcceleration;
    document.getElementById("direction").innerText = data.direction;
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