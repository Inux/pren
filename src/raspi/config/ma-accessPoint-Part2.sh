#!/bin/bash
#Konfiguration des MasterPI
echo ""
echo "Configuration RPI-Master AccessPoint Part 2"
echo "========================"
echo ""
echo ""

#installation accesspoint in a standalone network
echo "Set Static IP"
echo ""
echo ""

sudo echo "interface wlan0
        static ip_address=192.168.4.1/24
        nohook wpa_supplicant" >> /etc/dhcpcd.conf 

sudo service dhcpcd restart
echo "IP Adress: 192.168.4.1"

#configuration DHCP Server
echo "Configuration DHCP Server"
echo ""
echo ""

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
echo "interface=wlan0      # Use the require wireless interface - 
      usually wlan0
      dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" > ~/dnsmasq.conf
sudo mv ~/dnsmasq.conf /etc/dnsmasq.conf

#configuration access point host software
echo "configuration access point host software"
echo ""
echo ""
echo "interface=wlan0
driver=nl80211
ssid=PrenMasterTeam28
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=Team28Master
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP" > ~/hostapd.conf
sudo mv ~/hostapd.conf /etc/hostapd/hostapd.conf

sudo sed -i 's/\#DEAMON_CONF=\"\"/DEAMON_CONF=\"/etc/hostapd/hostapd.conf\"/g' /etc/default/hostapd

    