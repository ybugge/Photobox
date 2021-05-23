# Fotobox
Die Software wurde für den Raspberry PI entwickelt. Getestet wurde es auf dem Raspberry Pi 3 Model B+.
Entwickelt wurde es mit PyCharm in LinuxMint. Unter Windows funktioniert die Software nicht, da CUPS nicht von 
Windows unterstützt wird.

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
   - Tab -> "System"
   - Aktivieren: "Auf Netzwerk warten"
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
$ ./setupPhotobox.sh
````

Netzwerk nach einer Minute neu starten:
````
$ sudo crontab -e
@reboot /bin/sleep 60; /home/pi/Photobox/ShellScripts/restartNetwork.sh
STR+X -> Y -> ENTER 
````

##Drucker einrichten: Canon SELPHY CP1300 (W-LAN)
Quelle: 
- https://raspberrytips.com/install-printer-raspberry-pi/
- https://youtu.be/Gd0RKYRNJmo?t=570

PPD-Profile:
- 1.) https://cloud.voss.earth/index.php/s/SAi2M2na5KtR3gm -> https://www.voss.earth/2018/08/31/kurztipp-canon-selphy-wlan-drucker-cp910-oder-cp1300-unter-linux-cups-verwenden/
- 2.) https://www.objektiv-guide.de/icc-profil-canon-selphy/ -> Forum: https://www.dslr-forum.de/showthread.php?s=c6704e889a4db8e35e09f900192a341d&t=1865472&page=4

Browser->Pi: localhost:631

- Drucker und Klassen hinzufügen
- Drucker hinzufügen
- Eingabe: Benutzername und Passwort
- Drucker auswählen: (Netzwerkdrucker) Canon SELPHY CP1300 (Canon SELPHY CP1300)  
- Weiter
- Weiter
- PPD-Datei: Datei auswählen
- Photobox/PrinterPPD/Canon_SELPHY_CP1300.ppd
- Öffnen
- Drucker hinzufügen
- Color Mode: Color
- Media Size: Postcard.Fullbleed
- MediaType: Any
- Standardeinstellungen festlegen 

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

-> Auflösung: 1280x720
# Zusätzliche Hinweise:

# Musikserver:
## Bluetoothe Geräte verbinden (Allgemein)
Quellen:
- https://raspberrydiy.com/connect-raspberry-pi-bluetooth-speaker/

Auf dem Raspberry Pi (Oberfläche):
- Bluetooth-Symbol klicken
- Add Device
- Bluetoothgerät auswählen 
- Auf dem Lautspächer-Symbol rechtsklick
- Bluetoothgerät auswählen


##Mopidy
Quellen: 
- https://www.pcwelt.de/a/musikserver-mopidy-auf-raspberry-pi,3447697
- https://braspi.de/blogs/braspi-blog/raspberry-pi-als-musik-server-mit-mopidy
- https://magpi.raspberrypi.org/articles/make-a-raspberry-pi-audio-player-with-mopidy-music
- https://wiretuts.com/installing-mopidy-music-server-on-raspberry-pi
- https://docs.mopidy.com/en/latest/installation/raspberrypi/#how-to-for-raspbian
- Mopidy Local: https://pypi.org/project/Mopidy-Local/
- Permission denied: https://discourse.mopidy.com/t/mopidy-scan-usb-not-successful/4722/5
- https://discourse.mopidy.com/t/iris-and-mopidy-mobile-are-empty-when-music-is-on-usb-drive/4280/4
- Mopidy Error: https://discourse.mopidy.com/t/problem-scanning-local-flac-files/4823/3

###Wichtige Befehle:
- Konfiguration anzeigen:
````
$ sudo mopidyctl config
````
- Konfiguration anpassen:
````
$ sudo nano /etc/mopidy/mopidy.conf
````
- Serverstatus anzeigen
````
$ sudo systemctl status mopidy
````
- Starten/ Stoppen / Restart Server
````
$ sudo systemctl start/stop/restart mopidy
````
- Lokale Konfiguration anzeigen: (Template)
````
$ sudo nano /home/pi/.config/mopidy/mopidy.conf
````

### Instalation
Auf dem Raspberry Pi (SSH-Terminal):

````
$ sudo apt update
$ yes | sudo apt upgrade
USB-Stick, auf die die Musik vorhanden ist, einstecken. (Format: Fat32)
$ ls -l /dev/disk/by-label/
$ ls -l /dev/disk/by-uuid/
- UUID von Musikstick raus suchen: Bsp: FA43-EF95
$ sudo nano /etc/fstab
UUID=FA43-EF95 /media/usbMusic vfat auto,nofail,umask=000,noatime,users,rw,uid=mopidy,gid=audio 0 0
$ sudo reboot

$ wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
$ sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
$ sudo apt update
$ sudo apt install mopidy python3-pip libspotify-dev
$ sudo python3 -m pip install Mopidy-Youtube Mopidy-Local Mopidy-MusicBox-Webclient Mopidy-TuneIn
$ sudo adduser mopidy video
$ sudo nano /etc/mopidy/mopidy.conf

[http]
enabled = true
hostname = photobox.fritz.box
port = 6680

[audio]
#output = pulsesink server=127.0.0.1

[file]
enabled = true
media_dirs = /media/usbMusic|Home

[youtube]
enabled = false

[local]
enabled = true
media_dir = /media/usbMusic

[musicbox_webclient]
enabled = true
#musicbox = false

$ sudo mopidyctl config
$ sudo systemctl enable mopidy
$ sudo systemctl start mopidy
$ sudo systemctl status mopidy
- No Errors
$ mopidy local scan
$ sudo reboot
````

Im Browser: http://photobox.fritz.box:6680/mopidy/
Mit BluetoothBox:

Quelle: 
- https://wiretuts.com/connecting-bluetooth-audio-device-to-raspberry-pi
- https://www.wiretuts.com/connect-mopidy-to-bluetooth-speaker-on-raspberry-pi
````
Bluetooth gerät wir oben beschrieben mit Pi verbinden
$ sudo apt-get install pulseaudio*
$ sudo usermod -a -G lp pi
$ sudo reboot
$ sudo nano /etc/pulse/default.pa
- native-protocol-tcp -> Zwischenablage (Strg+C)
- Strg+W -> Strg+Umschalt+V 
- ersetzen mit -> load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1
- Strg+X -> Y -> ENTER
$ sudo nano /etc/mopidy/mopidy.conf
[audio]
output = pulsesink server=127.0.0.1
$ pulseaudio -k
$ pulseaudio --start
$ sudo reboot
````

Dienst nach einereinhalb Minute neu starten:
````
$ sudo crontab -e
@reboot /bin/sleep 90; sudo systemctl restart mopidy
STR+X -> Y -> ENTER 
````

Weiterer Adons:
- https://mopidy.com/ext/tunein/
- https://mopidy.com/ext/spotify/ 
- YoutubeAPI:
  - https://www.youtube.com/watch?v=ozOmQGDVwKQ

#TODO:
## Fehler:
- Diashow:
-- Bildverhältnis passt nicht
-- Sollen die Bilder wirklich gestretcht werden?