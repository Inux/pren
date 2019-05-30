#Deploy
#
IP="192.168.1.107" #IP Raspi
USR="pi"
PWD='raspberry'

#delete files/folders on raspi
sshpass -p $PWD ssh $USR@$IP 'sudo rm -rf ~/team28'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28/src'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28/src/raspi'

#copy bashrc to rasp (disabled by default)
#sshpass -p $PWD scp config/.bashrc $USR@$IP:~/.bashrc

#copy application to raspi
sshpass -p $PWD scp -r config $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r lib $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r numberdetector $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r pb $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp __init__.py $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp requirements.txt $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp run_slave.sh $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp setup.sh $USR@$IP:~/team28/src/raspi