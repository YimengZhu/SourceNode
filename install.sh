#Shellscript to install all the dependencies for the sourcing node 

#!/bin/bash

##################################################################
#Install the mosquitto and paho client
#Add the latest version of mosquitto to the apt archives.
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
apt-get update
apt-get install mosquitto

#Install the moquitto, mosquitto-clients, mosquitto python bindings
apt-get install mosquitto mosquitto-clients python-mosquitto

#After install, the broker is started immediately. Stop it to configure the broker
sudo /etc/init.d/mosquitto stop

#Configure the mosquitto server
sed -c -i "s/\(log_dest *  *\).*/\1 topic/" /etc/mosquitto/conf
echo "log_type error" >> /etc/mosquitto/conf
echo "log_type warning" >> /etc/mosquitto/conf
echo "log_type notice" >> /etc/mosquitto/conf
echo "log_type information" >> /etc/mosquitto/conf
echo "connection_messages true" >> /etc/mosquitto/conf
echo "log_timestamp true" >> /etc/mosquitto/conf

/etc/init.d/mosquitto start


##############################################################
#Install the gps dependencies
apt-get install gpsd gpsd-clients cmake subversion build-essential espeak freeglut3-dev imagemagick libdbus-1-dev libdbus-glib-1-dev libdevil-dev libfontconfig1-dev libfreetype6-dev libfribidi-dev libgarmin-dev libglc-dev libgps-dev libgtk2.0-dev libimlib2-dev libpq-dev libqt4-dev libqtwebkit-dev librsvg2-bin libsdl-image1.2-dev libspeechd-dev libxml2-dev ttf-liberation
echo "core_freq=250" /boot/config.txt
echo "enable_uart=1" /boot/config.txt
echo "dwc_otg.lpm_enable=0  console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4  elevator=deadline fsck.repair=yes   rootwait" > /boot/cmdline.txt
systemctl stop serial-getty@ttyS0.service
systemctl disable serial-getty@ttyS0.service
systemctl stop gpsd.socket
systemctl disable gpsd.socket

#TODO: Set the script continue after rebooting
reboot

#Excute the daemon reset
killall gpsd
gpsd /dev/ttyS0 -F /var/run/gpsd.sock

###############################################################
#Install the dependencies for weather station
pip install --upgrade pip
#Install the module provides the information on local time zone
pip install tzlocal
#Install the USB library
apt-get install libusb-1.0-0-dev
pip install libusb1
#Daemon process in unix 
pip install python-daemon
pip install paho-mqtt