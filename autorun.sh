#!/bin/bash
#This bash call by /home/pi/.config/autostart/autoboot.desktop

cd /home/pi
sudo python3 /home/pi/InformationSystem.py >information.txt
sudo chmod =777 information.txt

#sudo python3 /home/pi/NetworkStatus.py
#chmod =777 networkstatus.txt

sudo python3 /home/pi/reportip.py
#sudo chmod =766 powerupip.txt

#cd /home/pi/SteppingMotorWeb
#sudo python3 /home/pi/SteppingMotorWeb/DualAtepperWeb.py

exit 0