#Run PC Applications
echo "Starting Pc Applications..."

trap 'killall' INT

killall() {
    trap '' INT TERM
    echo "**** Shutting down... ****"
    kill -TERM 0
    wait
    echo DONE
}

# acoustic

#echo "...Acoustic..."
#python acoustic/sound.py &

# linedetector
echo "...LineDetector..."
python linedetector/fakelinedetector.py &

# movement
echo "...Movement..."
python movement/movement.py &

# numberdetector

#echo "...NumberDetector..."
#python numberdetector/numberDetectionPython/numberDetection.py &

# controlflow
echo "...ControlFlow..."
python controlflow/controlflow.py &

# webapp
echo "...WebApp..."
python webapp/server.py &

if [ socat ]
then
    socat -d -d pty,raw,echo=0 pty,raw,echo=0 &
fi

cat # wait forever
