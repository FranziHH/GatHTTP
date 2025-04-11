#!/bin/bash

lf=$(pwd)
cd ~/src
~/src/getHost.py "$@"
cd $lf
