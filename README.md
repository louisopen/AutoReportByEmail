## Auto report your IP to email
In Raspbian Desktop System

### auto boot this program after power up, as below  

sudo nano /home/pi/.config/autostart/autoboot.desktop	    #create file autoboot. (like rc.local)
[Desktop Entry]
Type=Application
Name=testboot
NoDisplay=true
Exec=/home/pi/autorun.sh

sudo nano /home/pi/autorun.sh	    #create file autorun.sh ()
#!/bin/bash
cd /home/pi
sudo python3 /home/pi/InformationSystem.py >information.txt
sudo chmod =766 information.txt
sudo python3 /home/pi/reportip.py
#sudo chmod =766 powerupip.txt
exit 0

### if you want to try the other auto-run 

sudo nano /etc/crontab              #add on line in crontab for running at 30 second after reboot 
@reboot sleep 30 ; /home/pi/autorun.sh

### Notice

The email config should be settings,**DO NOT** leave anything about your real e-mail on github,commit.