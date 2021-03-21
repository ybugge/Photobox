# Fotobox

## Hardware
- Raspberry Pi 3 Model B+ -> https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/
- Raspberry Pi High Quality Camera -> https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/
- Raspberry Pi Touch Display -> https://www.raspberrypi.org/products/raspberry-pi-touch-display/
- 16 GB SD-Karte
- Mini Wireless Keyboard Remote X8 -> http://www.riitek.com/product/x8.html
- Fritz!Box 4020 -> https://avm.de/produkte/fritzbox/fritzbox-4020/
- Canon SELPHY CP1300 -> https://www.canon.de/printers/selphy-cp1300/


##Install
Die nachfolgende Instalation wurde mit LinuxMint durchgeführt.
Der Raspberry Pi wird ab jetzt Pi genannt. 

Auf LinuxMint:
````
$ sudo apt update
$ yes | sudo apt install rpi-imager
$ rpi-image
````
- Operation Systenm = Raspberry PI OS (32-bit) (Recommanded)
- SD Card = Die zu verwendete SD-Karte
- "Write"
- "Yes"
- SD-Karte entnehmen und in den Pi stecken
- Raspberry Pi einschalten

Auf Raspberry Pi:
- Welcome to Raspberry Pi:
  - IP-Adresse aufschreiben: 192.168.188.22
  - Klicken: "Next"
  - Sprache einstellen und "Next" 
  - neues Passwort vergeben und "Next"
  - Bildschirmeinstellungen -> "Next"
  - Wifi eingeben wenn nötig. In meinem Fall ist der Pi mit dem Router über LAN verbunden 
  - Updates -> Next 
  - Pi neustarten 
 - Starten: "Raspberry-Pi-Konfiguration" unter "Start > Einstellungen"
   - Tab -> "Schnittstellen"
   - Aktivieren: "Kamera"
   - Aktivieren: "SSH"
   - Tab -> "Display"
   - Deaktivieren: "Screen Blanking"
   - "OK"
   - Restart? -> "Ja"
  
Auf der Fritzbox
- LinuxMint: mit der Fritzbox verbinden
- Browser öffnen und die Seite "fritz.box/" aufrufen
- Einloggen
- Heimnetz > Netzwerk > Pi raussuchen bsp:192.168.188.22 > Auf "Stift" klicken
- "Name" = photobox
- Aktivieren: "Diesem Netzwerkgerät immer die gleiche IPv4-Adresse zuweisen."
- "OK"

Auf LinuxMint:
- Terminal öffnen 
````
$ ssh pi@photobox.fritz.box
$ yes
$ -> Passwort eingeben 
$ sudo apt update
$ yes | sudo apt upgrade 
$ yes | sudo apt install git
$ git clone https://github.com/ybugge/Photobox.git
$ cd Photobox
$ ./setupFotobox.sh
````

# Diashow Client

## Hardware
- Raspberry Pi Zero W -> https://www.raspberrypi.org/products/raspberry-pi-zero-w/
- 16GB SD-Karte
- TV

## Install
Die nachfolgende Instalation wurde mit LinuxMint durchgeführt.
Der Raspberry Pi Zero W wird ab jetzt Pi genannt. 

Auf LinuxMint:
````
$ sudo apt update
$ yes | sudo apt install rpi-imager
$ rpi-image
````
- Operation Systenm = Raspberry PI OS (32-bit) (Recommanded)
- SD Card = Die zu verwendete SD-Karte
- "Write"
- "Yes"
- SD-Karte erneut in LinuxMint stecken
  - Ordner "boot" öffnen 
  - Datei "ssh" erstellen
  - Datei "wpa_supplicant.conf" erstellen 
  - folgendes eintragen: siehe https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```
- SD-Karte entnehmen und in den Pi stecken
- Raspberry Pi einschalten

Auf Linux Mint:
- Terminal öffnen:
````
$ ssh pi@<ip-adresse>
$ yes
$ password = raspberry
$ sudo raspi-config
System Options > Password > "Durchführen"
System Options > Network at Boot > Yes
Display Options > Underscan > No 
Display Options > Screen Blanking > No
Finish
Reboot > Yes
$ git clone https://github.com/ybugge/Photobox.git
$ cd Photobox
$ ./setupDiashow.sh
````
