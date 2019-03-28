#Run Raspi Applications
echo "Starting Raspi Applications..."

CURRENT_LOC=pwd
PYTHONPATH=$CURRENT_LOC/acoustic:$CURRENT_LOC/config:$CURRENT_LOC/controlflow:$CURRENT_LOC/lib:$CURRENT_LOC/linedetector:$CURRENT_LOC/movement:$CURRENT_LOC/numberdetector:$CURRENT_LOC/pb:$CURRENT_LOC/webapp

#webapp
echo "...WebApp..."
(cd webapp && python3 server.py) &

#vision
echo "...FakeLineDetector..."
(cd vision/linedetector && python3 fakelinedetector.py) &

#acustic