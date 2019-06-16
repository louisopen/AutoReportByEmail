#!/bin/bash
#This bash called by /home/pi/.config/autostart/autoboot.desktop
jump_dir=/home/pi
#tr -d "\r" < oldname.sh > newname.sh   #if you can't cd to .... just do this command.
cd $jump_dir
pwd
sudo python3 $jump_dir/InformationSystem.py >information.txt
sudo chmod =766 information.txt
#sudo python3 $jump_dir/NetworkStatus.py
#chmod =766 networkstatus.txt

sudo python3 $jump_dir/reportip.py
#sudo chmod =766 powerupip.txt

#cd $jump_dir/SteppingMotorWeb
#sudo python3 $jump_dir/SteppingMotorWeb/DualAtepperWeb.py

exit 0
