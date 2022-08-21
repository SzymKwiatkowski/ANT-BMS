apt update && apt upgrade -y && apt-get update && apt-get upgrade -y

apt install curl -y
apt install python2 -y
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add
echo "deb
https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
apt-get update
apt-get install python-pip
apt-get install python2-dev
pip install ipython
apt-get install libbluetooth-dev
apt-get install bluetooth
apt install git
git clone https://github.com/karulis/pybluez.git
cd pybluez
python2 setup.py install
apt-get update
apt update
apt-get install influxdb
apt-get install chronograf
apt-get install nodered
pip install requests
pip install serial



