#!/bin/bash

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install python3 python3-pyqt5 python3-pyqt5.qtwebkit python3-pip python3-opencv python3-pyqt5.qtmultimedia

echo "Start Configuration"
echo "sh ~/Photobox/ShellScipts/autostartDiashow.sh" >> ~/.bashrc