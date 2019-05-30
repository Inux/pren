#Run Raspi (Slave) Applications
echo "Starting Raspi (Slave) Applications..."

rm SoulTrain.log || true #delete log

trap 'killall' INT

killall() {
    trap '' INT TERM
    echo "**** Shutting down... ****"
    kill -TERM 0
    wait
    echo DONE
}

#numberdetection
echo "...Numberdetection..."
python3 numberdetector/Ablauf.py &

cat # wait forever
