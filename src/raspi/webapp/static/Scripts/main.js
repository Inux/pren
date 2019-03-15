//Variables & Constants
            var updateInterval = 500 // 500ms
            var isSimulating = false;
            var simulationIntervalID;

            //set values to initial value
            document.getElementById("direction").innerText = "undefined";

            //Helpers
            function apiGet(callback) {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                        console.log('responseText:' + xmlhttp.responseText);
                        try {
                            var data = JSON.parse(xmlhttp.responseText);
                        } catch(err) {
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
                updateDirection(data.direction);
            }

            function updateDirection(direction) {
                document.getElementById("direction").innerText = direction;
            }

            //Plays the number pressed as sound (e.g. for #1 it plays "Number one") wow
            function playSound(sound_nr){
                xmlhttp = new XMLHttpRequest()
                xmlhttp.open('GET', '/sound/' + sound_nr, true)
                xmlhttp.send()
                alert("playing Sound #1")
            }

            //Starts/stops simulation mode. Constantly updates movement values during simulation
            function start() {

                if(!isSimulating){
                    $("#Simulate").html('Stop');
                    movementSet();
                    simulationIntervalID = setInterval(movementGet, updateInterval, updateMovement);
                    isSimulating = true;
                } else {
                    $("#Simulate").html('Start');
                    clearInterval(simulationIntervalID);
                    isSimulating = false;
                }
            }

            // gets movement values (Acceleration, Speed, Distance) in a 500ms interval
            function movementGet(callback){
                var xhr = new XMLHttpRequest();
                var url = "/simulation/get";
                xhr.open("GET", url, true);
                xhr.setRequestHeader("Content-Type", "application/json");

                xhr.onreadystatechange = function(){
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        var json = JSON.parse(xhr.responseText);
                        console.log(json.acc + json.speed + json.distance );
                        callback(json);
                    }
                }

                xhr.send();

            }

            //callback of movementGet, sets the movement values
            function updateMovement(json) {
                $('#Acceleration').val(json.acc);
                $('#Speed').val(json.speed);
                $('#Distance').val(json.distance);
            };

            //setInterval(apiGet, updateInterval, updateUI);
            setInterval(apiGet, updateInterval, )