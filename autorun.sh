#!/bin/bash
#This bash called by autoboot.desktop or rootcron   #autoboot.desktop存放到/home/pi/.config/autostart/   #in X windows
#chmod =755 autoboot.desktop
#sudo nano .bashrc   	#最後行添加 sh autorun.sh   #同時(近端/遠端)啟動, Command line mode
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

jump_dir=/home/pi/BCON_MP
python /home/pi/stats.py &
cd $jump_dir
#tr -d "\r" < autorun.sh > newname.sh    #if you can't cd to .... just do this command. #置入新系統時若發生此訊息
#tr -d "\r" < autorun.sh > newname.sh    #if you got ...Syntax error: end of file unexpected (expecting "then")
#chmod =755 autorun.sh
pwd
sudo python3 $jump_dir/InformationSystem.py >information.txt
#sudo chmod =755 InformationSystem.py
sudo chmod =766 information.txt
#sudo python3 $jump_dir/NetworkStatus.py
#chmod =766 networkstatus.txt

sudo python3 $jump_dir/reportip.py
#sudo chmod =755 reportip.py
#sudo chmod =766 powerupip.txt

#cd $jump_dir/SteppingMotorWeb
#sudo python3 $jump_dir/SteppingMotorWeb/DualAtepperWeb.py

cd /home/pi
exit 0