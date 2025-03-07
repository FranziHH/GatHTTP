#!/bin/bash

if [ "$#" -gt "0" ]; then
    NEW_HOSTNAME="$1"
else
    echo "There is no new Name"
    exit 1
fi

CURRENT_HOSTNAME=$(cat /etc/hostname)

if [ $NEW_HOSTNAME = $CURRENT_HOSTNAME ]; then
    echo "Name already set"
else
    echo "Setting Name" $NEW_HOSTNAME
    echo $NEW_HOSTNAME | sudo tee /etc/hostname
    sudo sed -i "/127.0.1.1/s/$CURRENT_HOSTNAME/$NEW_HOSTNAME/" /etc/hosts
    sudo hostnamectl set-hostname $NEW_HOSTNAME
    sudo systemctl restart avahi-daemon
    /home/dev/GatHTTP/getHost.sh
    echo
    echo "Please Reboot (sudo reboot)"
fi
