#!/bin/bash
echo "Enabling Camera"
#yes, 0=on, 1=off
sudo raspi-config nonint do_camera 0

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install python3 python3-picamera python3-pyqt5 python3-pyqt5.qtwebkit git python3-pip python3-opencv python3-pyqt5.qtmultimedia cups python3-dev libcups2-dev

pip3 install qrcode
pip3 install numpy
pip3 install flask
pip3 install pysqlite3
pip3 install image
pip3 install pycups

#printer
sudo usermod -a -G lpadmin pi
sudo systemctl restart cups

#https://webnist.de/autostart-eines-python-programm-auf-dem-raspberry-pi/
echo "Start Configuration"
AUTOSTART_DIR="/home/pi/.config/autostart"
mkdir -p -- "$AUTOSTART_DIR"

AUTOSTART_FILE_SOURCE="/home/pi/Photobox/ShellScripts/autostartPhotobox.desktop"
AUTOSTART_FILE_DESTINI="/home/pi/.config/autostart/autostartPhotobox.desktop"
cp -vn $AUTOSTART_FILE_SOURCE $AUTOSTART_FILE_DESTINI

DESKTOP_FILE_DESTINI="/home/pi/Desktop/Photobox.desktop"
cp -vn $AUTOSTART_FILE_SOURCE $DESKTOP_FILE_DESTINI