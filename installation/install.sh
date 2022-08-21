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
#apt-get install chronograf -y
#apt-get install nodered -y
pip install requests
pip install serial



