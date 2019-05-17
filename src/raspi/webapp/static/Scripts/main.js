//Variables & Constants
let updateInterval = 250; // 250ms
let isSimulating = true;
let simulationIntervalID;

const COMMAND_START = 'start';
const COMMAND_STOP = 'stop';

/* Main functions ----------------------------- */

// Initialization
function init() {
    if (isSimulating) {
        enableSimulation();
        sendSpeed(0); // send speed 0
    } else {
        enableControlFlow();
    }
}

// Enable simulation mode, disable controlflow
function enableSimulation() {
    //Update Status to "Simulating"
    var state = document.getElementById('webAppState');
    state.innerHTML = "Simulating"

    //Remove ControlFlow from View
    var controlFlow = document.getElementById('controlFlow');
    controlFlow.style.display = 'none';

    //Enable Simulation View
    var simulation = document.getElementById('simulation');
    simulation.style.display = 'block';
}

// Enable controlflow, disable simulation mode
function enableControlFlow() {
    //Update Status to "ControlFlow"
    var state = document.getElementById('webAppState');
    state.innerHTML = "ControlFlow"

    //Remove Simulation from View
    var simulation = document.getElementById('simulation');
    simulation.style.display = 'none';

    //Enable ControlFlow View
    var controlFlow = document.getElementById('controlFlow');
    controlFlow.style.display = 'block';
}

function getControlFlowData(command) {
    let data = {};

    //startup and finished have to be executed anyway!
    // -startup is always executed when starting (finished as well)
    // -finished is always executed when pressing stop
    data = {
        "command": command,
        "phases": {
            "startup": true,
            "find_cube": document.getElementById("find_cube").checked,
            "grab_cube": document.getElementById("grab_cube").checked,
            "round_one": document.getElementById("round_one").checked,
            "round_two": document.getElementById("round_two").checked,
            "find_stop": document.getElementById("find_stop").checked,
            "stopping": document.getElementById("stopping").checked,
            "finished": true,
        }
    };

    return data;
}

function sendControlFlowData(data) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('POST', '/controlflow', true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify(data));
}

// start ControlFlow
function startControlFlow() {
    sendControlFlowData(getControlFlowData(COMMAND_START));
}

// stop ControlFlow
function stopControlFlow() {
    sendControlFlowData(getControlFlowData(COMMAND_STOP));
}


/* Simulation commands ------------------------ */

// Plays the number pressed as sound (e.g. for #1 it plays "Number one") wow
function playSound(sound_nr) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/sound/' + sound_nr, true);
    try {
        xmlhttp.send();
    } catch(e) {
        console.error("could not play sound:", e)
    }
}

function sendSpeed(speed) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/speed/' + speed, true);
    try {
        xmlhttp.send();
    } catch(e) {
        console.error("could not send speed:", e)
    }
}

function moveStart() {
    var speedValue = document.getElementById("speedValue").value;
    sendSpeed(speedValue);
}

function moveStop() {
    var speedValue = document.getElementById("speedValue");
    speedValue.value = 0;
    sendSpeed(0);
}

/* Events ------------------------------------- */

simMode = document.getElementById('simMode');
simMode.onchange = (e) => {
    e.preventDefault();

    if (e.target.checked) {
        isSimulating = true;
    } else {
        isSimulating = false;
    }

    init();
};

let sound = document.getElementById('sound');
sound.onchange = () => {
    soundValue = document.getElementById("soundValue");
    soundStatus = document.getElementById("soundStatus");
    soundValue.innerHTML = sound.value;
    soundStatus.innerHTML = "selected number " + soundValue.innerHTML;
};
sound.onchange();

let soundButton = document.getElementById('soundButton');
soundButton.onclick = () => {
    soundValue = document.getElementById("soundValue");
    soundStatus = document.getElementById("soundStatus");
    playSound(soundValue.innerHTML);
    soundStatus.innerHTML = "played number: " + soundValue.innerHTML;
};

let craneOnButton = document.getElementById('craneOn');
let craneResetButton = document.getElementById('craneReset');
craneOnButton.disabled = true;
craneResetButton.disabled = true;

let craneStatus = document.getElementById("crane");

craneOnButton.onclick = () => {
    if(document.getElementById("crane").innerText === "0") {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open('GET', '/crane/1', true);
        try {
            xmlhttp.send();
        } catch(e) {
            console.error("could not move crane:", e);
        }

        craneOnButton.disabled = true;
    }
};

craneResetButton.onclick = () => {
    if(document.getElementById("crane").innerText === "1") {
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open('GET', '/crane/0', true);
        xmlhttp.send();

        craneResetButton.disabled = true;
    }
};

/* Start Main Flow ---------------------------- */

// Call init the first time
init();