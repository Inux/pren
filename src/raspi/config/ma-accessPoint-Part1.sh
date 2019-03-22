#!/bin/bash
#Konfiguration des MasterPI
echo ""
echo "Configuration RPI-Master AccessPoint Part 1"
echo "========================"
echo ""
echo ""

# RPI update & upgrade
echo "1. update & upgrade RPI"
echo ""
echo ""
sudo apt update && upgrade -y
sleep 2

#installation accesspoint in a standalone network
echo "2. install accesspoint"
echo ""
echo ""
sudo apt install dnsmasq hostapd -y
sleep 2
sudo systemctl stop dnsmasq -y
sleep 2
sudo systemctl stop hostapd -y

sudo reboot



