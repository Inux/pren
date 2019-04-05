//Variables & Constants
var updateInterval = 500; // 500ms
var isSimulating = false;
var simulationIntervalID;

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

// UI

//updateUI method (called by setInterval each 500ms)
function updateUI(data) {
    console.log("Received Data:");
    console.log(data);

    updateSoulTrainData(data);
    updateHeartBeats(data);
}

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

function updateHeartBeats(data) {
    lineDetectionDiv = document.getElementById("lineDetectionDiv");
    numberDetectionDiv = document.getElementById("numberDetectionDiv");
    movementDiv = document.getElementById("movementDiv");
    acousticDiv = document.getElementById("acousticDiv");
    controlFlowDiv = document.getElementById("controlflowDiv");

    elements = [lineDetectionDiv, numberDetectionDiv, movementDiv, acousticDiv, controlFlowDiv];

    elements.forEach((item, index) => {
        if(item == null) {
            console.warn("Item " + index + " is null! cannot remove classes!")
        } else {
            item.classList.remove("starting", "running", "error", "finished");
        }
    });

    lineDetectionDiv.classList.add(data.heartBeatLineDetection);
    numberDetectionDiv.classList.add(data.heartBeatNumberDetection);
    movementDiv.classList.add(data.heartBeatMovement);
    acousticDiv.classList.add(data.heartBeatAcoustic);
    controlFlowDiv.classList.add(data.heartBeatControlFlow);
}

//Plays the number pressed as sound (e.g. for #1 it plays "Number one") wow
function playSound(sound_nr) {
    xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', '/sound/' + sound_nr, true)
    xmlhttp.send()
    alert("playing Sound #1")
}

// start ControlFlow
function start() {

}

setInterval(function(){
    apiGet(updateUI);
}, updateInterval);
