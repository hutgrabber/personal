#!/bin/bash

# This script will automagically install the tools
# for hutgrabber. Please run as root.


cat << "EOF"
  _           _                  _     _               
 | |         | |                | |   | |              
 | |__  _   _| |_ __ _ _ __ __ _| |__ | |__   ___ _ __ 
 | '_ \| | | | __/ _` | '__/ _` | '_ \| '_ \ / _ | '__|
 | | | | |_| | || (_| | | | (_| | |_) | |_) |  __| |   
 |_| |_|\__,_|\__\__, |_|  \__,_|_.__/|_.__/ \___|_|   
                  __/ |                                
                 |___/                                 
EOF

fail() {
	echo "$@, exiting," >&2
	exit 1
}

fail