#Run Raspi Applications
echo "Starting Raspi Applications..."

#webapp
echo "...WebApp..."
python3 webapp/server.py &

#vision
echo "...FakeLineDetector..."
python3 vision/linedetector/fakelinedetector.py &

#acustic