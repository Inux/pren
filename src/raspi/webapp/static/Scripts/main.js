//Variables & Constants
var updateInterval = 250; // 250ms
var isSimulating = true;
var simulationIntervalID;

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

// start ControlFlow
function startControlFlow() {

}


/* Simulation commands ------------------------ */

// Plays the number pressed as sound (e.g. for #1 it plays "Number one") wow
function playSound(sound_nr) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/sound/' + sound_nr, true);
    xmlhttp.send();
}

function sendSpeed(speed) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/speed/' + speed, true);
    xmlhttp.send();
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
    soundStatus = "played number: " + soundValue.innerHTML;
};

let craneOnButton = document.getElementById('craneOn');
craneOnButton.onclick = () => {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/crane/1', true);
    xmlhttp.send();
    craneOnButton.disabled = true;
};

let craneResetButton = document.getElementById('craneReset');
craneResetButton.onclick = () => {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET', '/crane/0', true);
    xmlhttp.send();
    craneOnButton.disabled = false;
};

/* Start Main Flow ---------------------------- */

// Call init the first time
init();