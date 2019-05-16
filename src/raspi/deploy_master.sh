#Deploy
#
IP="prenteam28master.local" #IP Raspi Master
USR="pi"
PWD='team28team$$'

#delete files/folders on raspi
sshpass -p $PWD ssh $USR@$IP 'sudo rm -rf ~/team28'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28/src'
sshpass -p $PWD ssh $USR@$IP 'mkdir -p ~/team28/src/raspi'

#copy bashrc to rasp (disabled by default)
#sshpass -p $PWD scp config/.bashrc $USR@$IP:~/.bashrc

#copy application to raspi
sshpass -p $PWD scp -r acoustic $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r config $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r controlflow $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r lib $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r linedetector $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r movement $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r numberdetector $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r pb $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp -r webapp $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp __init__.py $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp build.sh $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp kill.sh $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp requirements.txt $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp run_master.sh $USR@$IP:~/team28/src/raspi
sshpass -p $PWD scp setup.sh $USR@$IP:~/team28/src/raspi
