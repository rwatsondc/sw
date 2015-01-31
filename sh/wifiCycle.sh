#!/bin/bash
#take wifi down and bring back up after 5 seconds
ifconfig mlan0 down
sleep 5
ifconfig mlan0 up
