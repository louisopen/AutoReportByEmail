## Report your IP to email
auto boot my program after power up, as below  
sudo nano /home/pi/.config/autostart/autoboot.desktop	#create file autoboot.desktop
[Desktop Entry]
Type=Application
Name=testboot
NoDisplay=true
Exec=/home/pi/autorun.sh

sudo nano /home/pi/autorun.sh	#create file autorun.sh
#!/bin/bash
cd /home/pi
sudo python3 /home/pi/InformationSystem.py >information.txt
sudo chmod =777 information.txt
sudo python3 /home/pi/reportip.py
#sudo chmod =766 powerupip.txt
exit 0


### Notice

The email config should be settings,**DO NOT** leave anything about your real e-mail on github,commit.

## License

	The MIT License (MIT)
	
	Copyright (c) 2024
	
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.
