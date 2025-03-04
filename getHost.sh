#!/bin/bash

lf=$(pwd)
cd ~/GatHTTP
~/GatHTTP/getHost.py "$@"
cd $lf
