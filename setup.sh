# Wirklich benötigt
# sudo apt-get install libqt5multimedia5-plugins
# apt install pip3
# pip3 install PyQt5
# pip3 install opencv-python==4.1.0.25
#pip3 install opencv-python qrcode numpy
# sudo pip3 install flask
# sudo pip3 install cryptography
# sqlite3
# Image
#


# Vielleihct doch nicht
# sudo apt update
# sudo apt install libopencv-dev python3-opencv

###     git push -u -f origin master






git:
https://www.digitalocean.com/community/tutorials/how-to-push-an-existing-project-to-github
git push -u -f origin master


#!/bin/bash

echo "Enabling Camera"
#yes, 0=on, 1=off
sudo raspi-config nonint do_camera 0

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install openbox xorg python3 python3-picamera python3-pyqt5 python3-pyqt5.qtwebengine lightdm git
# Suggested tools: sxiv tmux vim usbmount x11vnc
'''
echo "Installing Fotobox"
git clone https://github.com/adlerweb/fotobox.git /home/pi/fotobox

echo "Configuring autostart"
mkdir -p ~/.config/openbox
echo "xset s noblank" >> ~/.config/openbox/autostart
echo "xset s off" >> ~/.config/openbox/autostart
echo "xset -dpms" >> ~/.config/openbox/autostart
echo "cd ~/fotobox/ ; python3 fotobox.py | tee fotobox.log" >> ~/.config/openbox/autostart
# GUI-Boot with autologin
sudo raspi-config nonint do_boot_behaviour B4

echo "Syncing..."
sudo sync
'''
