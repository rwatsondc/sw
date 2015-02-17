#!/bin/bash
echo "Running webLogCopy.sh"
python /home/pyTest/sParse.py
python /home/pyTest/sshLogBackup.py
