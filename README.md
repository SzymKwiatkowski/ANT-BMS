# ANT-BMS
BMS logging via bluetooth. Application dedicated for Raspberry Pi with ubuntu 22.04 OS. 
# Test image of ubuntu with docker
First use setup script and give it executable privilages if needed.
```bash
./test/setup.sh
```
After wards use:
```bash
sudo docker ps
```
To view current session of docker running in the background. Keep process id in mind it will also be displayed after you use setup script.
Installation file will automatically be moved into root section of docker so the only thing you will need to do is attach yourself to currently running docker with:
```bash
sudo docker exec -it ab12 /bin/bash 
```
Whereas ab12 is id of currently running process in hexadecimal. You can also use previously given name which by default will be named test. Alternatively you can use attach script.

To detach yourself from process enter exit command. Remember to delete install script with rm command before exiting. Keep in mind that you need to run copy script in test directory to upload new file to docker image.

To terminate docker session use 
```bash
sudo docker stop test
```
and then
```bash
sudo docker rm test
```

# RPI setup
`install.sh` prepares your RPI to flawlessly run python script  with required software (influxdB, grafana, cron)  
  
Make sure you are at `ANT-BMS` directory and give executable privileges with command

```bash
sudo chmod +x installation/install.sh
```
You need to switch into superuser mode by typing   


```bash
sudo su -
```
To start installation procces simply type
```bash
.installation/install.sh 
```
You may rest now, it will took a while. When everything is done you may leave superuser mode by typing `exit`.


## Bluetooth connection
To enter RPI bluetooth control center type:
```bash
sudo bluetoothctl
```
To scan nearby bluetooth devices use `scan on` command.  

**You need to be sure, that your BMS is active. It can enter hibernation once the main battery isn't charging/discharging.**

There should be two or three devices named `ANT-BLE` or `BMS-ANT`.  
Copy the MAC adress of `BMS-ANT` (the one with lower value at the end of adress). To pair with BMS run following command 
```bash
pair <insert mac adress here>
```
Default pin code is `1234`.  

After that, replace exemplary MAC adress in `bms_data.py` with the one you copied recently.

Now you can test communication by running pythone code
```bash
python2 bms_data.py
```

## Checkout
After running installation update job in crontab using root.txt and paste the job to /etc/crontab file. After doing so check if it's running with 
```bash
systemctl status cron
```

After that you can check grafana setting or edit them using in:
```bash
nano /etc/grafana/grafana.ini
```
This file will enable you to specify custom settings.
