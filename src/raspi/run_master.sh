#Run Raspi Applications
echo "Starting Raspi Applications..."

CURRENT_LOC=pwd
PARENT_LOC=$(pwd)"/.."
PARENT_PARENT_LOC=$(pwd)"/../.."
PYTHONPATH=$CURRENT_LOC/acoustic:$CURRENT_LOC/config:$CURRENT_LOC/controlflow:$CURRENT_LOC/lib:$CURRENT_LOC/linedetector:$CURRENT_LOC/movement:$CURRENT_LOC/numberdetector:$CURRENT_LOC/pb:$CURRENT_LOC/webapp:$PARENT_LOC:$PARENT_PARENT_LOC:$CURRENT_LOC:$PYTHONPATH

#linedetector
echo "...LineDetector..."
python3 linedetector/fakelinedetector.py &

#webapp
echo "...WebApp..."
python3 webapp/server.py &
