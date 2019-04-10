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
    var state = document.getElementById('webAppState');
    state.innerHTML = "Simulating"

    var controlFlow = document.getElementById('controlFlow');
    controlFlow.style.display = 'none';

    var simulation = document.getElementById('simulation');
    simulation.style.display = 'block';
}

// Enable controlflow, disable simulation mode
function enableControlFlow() {
    var state = document.getElementById('webAppState');
    state.innerHTML = "ControlFlow"

    var simulation = document.getElementById('simulation');
    simulation.style.display = 'none';

    var controlFlow = document.getElementById('controlFlow');
    controlFlow.style.display = 'block';
}

// start ControlFlow
function startControlFlow() {

}


/* Simulation commands ------------------------ */

// Plays the number pressed as sound (e.g. for #1 it plays "Number one") wow
function playSound(sound_nr) {
    xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', '/sound/' + sound_nr, true)
    xmlhttp.send()
    alert("playing Sound #1")
}

function sendSpeed(speed) {
    xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', '/speed/' + speed, true)
    xmlhttp.send()
}

function moveStart() {
    var speedValue = document.getElementById("speedValue").value
    sendSpeed(speedValue)
}

function moveStop() {
    var speedValue = document.getElementById("speedValue");
    speedValue.value = 0;
    sendSpeed(0);
}

/* Events ------------------------------------- */

simMode = document.getElementById('simMode');
simMode.addEventListener('change', e => {
    e.preventDefault();

    if (e.target.checked) {
        isSimulating = true;
    } else {
        isSimulating = false;
    }

    init();
});

/* Start Main Flow ---------------------------- */

// Call init the first time
init();