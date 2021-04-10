#!/bin/bash
cd /home/pi/Photobox/
git pull
OPENBLAS_MAIN_FREE=1 python3 photoboxMain.py