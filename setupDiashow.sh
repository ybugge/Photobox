#!/bin/bash

echo "Updating System"
sudo apt update
yes | sudo apt dist-upgrade

echo "Installing prerequirements"
yes | sudo apt install python3 python3-pyqt5 python3-pyqt5.qtwebkit python3-pip python3-opencv python3-pyqt5.qtmultimedia

echo "Start Configuration"
AUTOSTART_DIR="/home/pi/.config/autostart"
mkdir -p -- "$AUTOSTART_DIR"

AUTOSTART_FILE_SOURCE="/home/pi/Photobox/ShellScripts/autostartDiashow.desktop"
AUTOSTART_FILE_DESTINI="/home/pi/.config/autostart/autostartDiashow.desktop"
cp -vn $AUTOSTART_FILE_SOURCE $AUTOSTART_FILE_DESTINI

DESKTOP_FILE_DESTINI="/home/pi/Desktop/PhotoboxDiashow.desktop"
cp -vn $AUTOSTART_FILE_SOURCE $DESKTOP_FILE_DESTINI