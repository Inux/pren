#Run Raspi Applications
echo "Starting Raspi Applications..."

#linedetector
echo "...LineDetector..."
python3 linedetector/fakelinedetector.py &

#webapp
echo "...WebApp..."
python3 webapp/server.py &
