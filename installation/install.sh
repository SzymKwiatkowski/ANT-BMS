apt update && apt upgrade -y && apt-get update && apt-get upgrade -y

apt-get install -y gnupg2
apt install curl -y
apt install python2 -y
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py
curl -sL https://repos.influxdata.com/influxdb.key | apt-key add
echo "deb https://repos.influxdata.com/debian buster stable" | tee /etc/apt/sources.list.d/influxdb.list

apt-get update -y
apt-get install python-pip -y
apt-get install python2-dev -y
pip install ipython
apt-get install libbluetooth-dev -y
apt-get install bluetooth -y
apt install git -y
git clone https://github.com/karulis/pybluez.git
cd pybluez
python2 setup.py install
apt-get update -y
apt update -y
apt-get install influxdb -y
pip install requests
pip install serial

#apt install npm
#npm install -g --unsafe-perm node-red

wget https://dl.grafana.com/oss/release/grafana_6.7.3_armhf.deb
dpkg -i grafana_6.7.3_armhf.deb
/bin/systemctl enable grafana-server
/bin/systemctl start grafana-server

wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /etc/apt/trusted.gpg.d/influxdb.asc >/dev/null
source /etc/os-release
echo "deb https://repos.influxdata.com/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update -y && sudo apt-get install telegraf -y

apt-get install cron
