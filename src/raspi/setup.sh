#Raspi Setup
#
#1. install raspbian -> https://www.raspberrypi.org/downloads/raspbian/
#2. packages:
#   -sudo apt-get install python3-pip // Python3 and pip3
#   -sudo apt-get install lsof // used to find open ports (kill.sh)
#   -Middleware
#       -PROTOC_ZIP=protoc-3.3.0-linux-x86_64.zip
#       -curl -OL https://github.com/google/protobuf/releases/download/v3.3.0/$PROTOC_ZIP
#       -sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
#       -rm -f $PROTOC_ZIP
#3. wifi hotspot -> https://github.com/billz/raspap-webgui
#       - ssid: RaspiTeam28
#       - ip: 10.3.141.1
#       - usr: admin
#       - pwd: team28team$$
#4.
#5.
#6.

#pip packages
pip3 install -r requirements.txt