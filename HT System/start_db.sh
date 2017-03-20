#! /bin/bash
mongod.exe --dbpath ./db
bash -c 'gnome-terminal -x mongo'