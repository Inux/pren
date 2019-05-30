#Run Raspi Applications
echo "Starting Raspi Applications..."

rm SoulTrain.log || true #delete log

trap 'killall' INT

killall() {
    trap '' INT TERM
    echo "**** Shutting down... ****"
    kill -TERM 0
    wait
    echo DONE
}

#acoustic
echo "...Acoustic..."
python3 acoustic/sound.py &

#linedetector
echo "...LineDetector..."
python3 linedetector/fakelinedetector.py &

#movement
echo "...Movement..."
python3 movement/movement.py &

#controlflow
echo "...ControlFlow..."
python3 controlflow/controlflow.py &

#webapp
echo "...WebApp..."
python3 webapp/server.py &

cat # wait forever
