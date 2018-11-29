#Run Raspi Applications
echo "Starting Raspi Applications..."

#webapp
echo "...WebApp..."
(cd webapp && python3 server.py) &

#vision
echo "...FakeLineDetector..."
(cd vision/linedetector && python3 fakelinedetector.py) &

#acustic