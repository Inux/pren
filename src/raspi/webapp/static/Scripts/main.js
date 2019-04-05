//Variables & Constants
var updateInterval = 250; // 250ms
var isSimulating = false;
var simulationIntervalID;

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
