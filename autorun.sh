#!/bin/bash
#This bash called by autoboot.desktop or rootcron   #autoboot.desktop存放到/home/pi/.config/autostart/
jump_dir=/home/pi
cd $jump_dir
#tr -d "\r" < oldname.sh > newname.sh    #if you can't cd to .... just do this command. #置入新系統時若發生此訊息
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

exit 0
