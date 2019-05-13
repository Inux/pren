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
#3. wifi hotspot (hostapd)-> https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm
#4. sudo apt-get install -y i2c-tools
#5.
#6.

#pip packages
pip3 install -r requirements.txt
