#Deploy
#
IP="team28master" #IP Raspi in RaspiTeam28 Wlan
PWD='team28team$$'

#delete files/folders on raspi
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/acoustic'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/config'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/controlflow'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/lib'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/linedetector'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/movement'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/numberdetector'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/pb'
sshpass -p $PWD ssh pi@$IP 'rm -rf ~/team28/webapp'
sshpass -p $PWD ssh pi@$IP 'rm ~/team28/*'

#copy files to raspi
sshpass -p $PWD scp -r acoustic pi@$IP:~/team28
sshpass -p $PWD scp -r config pi@$IP:~/team28
sshpass -p $PWD scp -r controlflow pi@$IP:~/team28
sshpass -p $PWD scp -r lib pi@$IP:~/team28
sshpass -p $PWD scp -r linedetector pi@$IP:~/team28
sshpass -p $PWD scp -r movement pi@$IP:~/team28
sshpass -p $PWD scp -r numberdetector pi@$IP:~/team28
sshpass -p $PWD scp -r pb pi@$IP:~/team28
sshpass -p $PWD scp -r webapp pi@$IP:~/team28
sshpass -p $PWD scp __init__.py pi@$IP:~/team28
sshpass -p $PWD scp build.sh pi@$IP:~/team28
sshpass -p $PWD scp deploy_master.sh pi@$IP:~/team28
sshpass -p $PWD scp kill.sh pi@$IP:~/team28
sshpass -p $PWD scp requirements.txt pi@$IP:~/team28
sshpass -p $PWD scp run_master.sh pi@$IP:~/team28
sshpass -p $PWD scp setup.sh pi@$IP:~/team28
