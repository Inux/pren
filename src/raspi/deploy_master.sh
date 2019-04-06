#Deploy
#
IP="team28master" #IP Ras$USR in Ras$USRTeam28 Wlan
USR="root"
PWD='team28team$$'

#delete files/folders on raspi
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/acoustic'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/config'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/controlflow'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/lib'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/linedetector'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/movement'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/numberdetector'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/pb'
sshpass -p $PWD ssh $USR@$IP 'rm -rf ~/team28/webapp'
sshpass -p $PWD ssh $USR@$IP 'rm ~/team28/*'

#copy files to raspi
sshpass -p $PWD scp -r acoustic $USR@$IP:~/team28
sshpass -p $PWD scp -r config $USR@$IP:~/team28
sshpass -p $PWD scp -r controlflow $USR@$IP:~/team28
sshpass -p $PWD scp -r lib $USR@$IP:~/team28
sshpass -p $PWD scp -r linedetector $USR@$IP:~/team28
sshpass -p $PWD scp -r movement $USR@$IP:~/team28
sshpass -p $PWD scp -r numberdetector $USR@$IP:~/team28
sshpass -p $PWD scp -r pb $USR@$IP:~/team28
sshpass -p $PWD scp -r webapp $USR@$IP:~/team28
sshpass -p $PWD scp __init__.py $USR@$IP:~/team28
sshpass -p $PWD scp build.sh $USR@$IP:~/team28
sshpass -p $PWD scp deploy_master.sh $USR@$IP:~/team28
sshpass -p $PWD scp kill.sh $USR@$IP:~/team28
sshpass -p $PWD scp requirements.txt $USR@$IP:~/team28
sshpass -p $PWD scp run_master.sh $USR@$IP:~/team28
sshpass -p $PWD scp setup.sh $USR@$IP:~/team28
