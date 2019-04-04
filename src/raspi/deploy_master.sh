#Deploy
#
IP="10.3.141.1" #IP Raspi in RaspiTeam28 Wlan
PWD="raspberry"

#delete files/folders on raspi
ssh pi@$IP 'rm -rf ~/team28/webapp'

#copy files to raspi
scp -r webapp pi@$IP:~/team28
scp kill.sh pi@$IP:~/team28
scp requirements.txt pi@$IP:~/team28
scp run.sh pi@$IP:~/team28
scp setup.sh pi@$IP:~/team28
