#!/bin/bash
sudo docker run -td --name="test" -p 127.0.0.1:80:80 ubuntu:22.04

sudo docker cp ./installation/install.sh test:/
sudo docker cp ./bms_data.py test:/