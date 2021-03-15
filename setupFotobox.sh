#!/bin/bash
echo "Enabling Camera"
#yes, 0=on, 1=off
sudo raspi-config nonint do_camera 0

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install python3 python3-picamera git python3-pip
sudo python3 -m pip install -U pip
sudo python3 -m pip install -U setuptools
pip3 install PyQt5
pip3 install opencv-python==4.1.0.25
pip3 install qrcode
pip3 install numpy
pip3 install flask
pip3 install pysqlite3
pip3 install image
pip3 install opencv-python