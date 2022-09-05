import socket
import time
import requests as req
from binascii import unhexlify
import struct
import sys
import serial
import bluetooth
from bluetooth import *
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

serverMACAddress = '20:A1:11:01:23:45'
port = 1
ser = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
ser.connect((serverMACAddress, port))

time.sleep(0.1)

url = "your url link for uploading data"
token = "put_your_api_token_here"
org = "Test"
bucket = "Pomiary"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
if not client.ping():
    raise Exception("Cannot connect to server")

test2 = '5A5A5A00005A'
test3 = 'DBDB00000000'
try:
    ser.send(test2.decode('hex'))
    time.sleep(0.005)
    ser.send(test3.decode('hex'))
    time.sleep(0.01)
except:
    ser.close()
time.sleep(1)
Antw33 = ser.recv(140)

#Reamining Ah
data_remaining_ah = (Antw33.encode('hex') [79*2:82*2+2])
try:
  data_remaining_ah = float.fromhex(data_remaining_ah)*0.000001
  print (data_remaining_ah)
  data_remaining_ah_str=''+str(data_remaining_ah)
except:
  pass

#SoC
bms_soc = (Antw33.encode('hex') [(74*2):(75*2)])
bms_soc=int(bms_soc,16)
print (bms_soc)
bms_soc_str=''+str(bms_soc)

#Power
bms_pow = (Antw33.encode('hex') [(111*2):(114*2+2)])
try:
    if int(bms_pow,16)>2147483648:
        bms_pow=(-(2*2147483648)+int(bms_pow,16))
        bms_pow = (bms_pow * -1)
        print (bms_pow)
    else:
        bms_pow=int(bms_pow,16)
        bms_pow=(bms_pow * -1)
        print (bms_pow)
except:
    pass

#BMS current
bms_current = (Antw33.encode('hex') [(70*2):(73*2+2)])
try:
    if int(bms_current,16)>2147483648:
        bms_current=(-(2*2147483648)+int(bms_current,16))*0.1
        bms_current=(bms_current * -1)
        print (bms_current)
        bms_current_str=''+str(bms_current)
    else:
        bms_current = int(bms_current,16)*0.1
        bms_current=(bms_current * -1)
        print (bms_current)
        bms_current_str=''+str(bms_current)

    #resp = req.get(url+'BMS_Current'+'?value='+str(bms_current))
except:
    pass

#BMS V
bms_v = (Antw33.encode('hex') [8:12])
bms_v = struct.unpack('>H',unhexlify(bms_v))[0]*0.1
bms_v = bms_v+0.0
#0.7 was added as BMS low.
print (bms_v)
bms_v_str=''+str(bms_v)

#Cell_avg
cell_avg = (Antw33.encode('hex') [(121*2):(122*2+2)])
cell_avg = struct.unpack('>H',unhexlify(cell_avg))[0]*0.001
print (cell_avg)
cell_avg_str=''+str(cell_avg)

#Cell_min
cell_min = (Antw33.encode('hex') [(119*2):(120*2+2)])
cell_min = struct.unpack('>H',unhexlify(cell_min))[0]*0.001
print (cell_min)
cell_min_str=''+str(cell_min)


#Cell_max
cell_max = (Antw33.encode('hex') [(116*2):(117*2+2)])
cell_max = struct.unpack('>H',unhexlify(cell_max))[0]*0.001
print (cell_max)
cell_max_str=''+str(cell_max)


#Cell_1
cell1 = (Antw33.encode('hex') [(6*2):(7*2+2)])
cell1 = struct.unpack('>H',unhexlify(cell1))[0]*0.001
print (cell1)
cell1_str=''+str(cell1)

#Cell_2
cell2 = (Antw33.encode('hex') [(8*2):(9*2+2)])
cell2 = struct.unpack('>H',unhexlify(cell2))[0]*0.001
print (cell2)
cell2_str=''+str(cell2)

#Cell_3
cell3 = (Antw33.encode('hex') [(10*2):(11*2+2)])
cell3 = struct.unpack('>H',unhexlify(cell3))[0]*0.001
print (cell3)
cell3_str=''+str(cell3)

#Cell_4
cell4 = (Antw33.encode('hex') [(12*2):(13*2+2)])
cell4 = struct.unpack('>H',unhexlify(cell4))[0]*0.001
print (cell4)
cell4_str=''+str(cell4)

#Cell_5
cell5 = (Antw33.encode('hex') [(14*2):(15*2+2)])
cell5 = struct.unpack('>H',unhexlify(cell5))[0]*0.001
print (cell5)
cell5_str=''+str(cell5)

#Cell_6
cell6 = (Antw33.encode('hex') [(16*2):(17*2+2)])
cell6 = struct.unpack('>H',unhexlify(cell6))[0]*0.001
print (cell6)
cell6_str=''+str(cell6)


#Cell_7
cell7 = (Antw33.encode('hex') [(18*2):(19*2+2)])
cell7 = struct.unpack('>H',unhexlify(cell7))[0]*0.001
print (cell7)
cell7_str=''+str(cell7)

#Cell_8
cell8 = (Antw33.encode('hex') [(20*2):(21*2+2)])
cell8 = struct.unpack('>H',unhexlify(cell8))[0]*0.001
print (cell8)
cell8_str=''+str(cell8)

#Cell_9
cell9 = (Antw33.encode('hex') [(22*2):(23*2+2)])
cell9 = struct.unpack('>H',unhexlify(cell9))[0]*0.001
print (cell9)
cell9_str=''+str(cell9)

#Cell_10
cell10 = (Antw33.encode('hex') [(24*2):(25*2+2)])
cell10 = struct.unpack('>H',unhexlify(cell10))[0]*0.001
print (cell10)
cell10_str=''+str(cell10)

#Cell_11
cell11 = (Antw33.encode('hex') [(26*2):(27*2+2)])
cell11 = struct.unpack('>H',unhexlify(cell11))[0]*0.001
print (cell11)
cell11_str=''+str(cell11)

#Cell_12
cell12 = (Antw33.encode('hex') [(28*2):(29*2+2)])
cell12 = struct.unpack('>H',unhexlify(cell12))[0]*0.001
print (cell12)
cell12_str=''+str(cell12)

#Cell_13
cell13 = (Antw33.encode('hex') [(30*2):(31*2+2)])
cell13 = struct.unpack('>H',unhexlify(cell13))[0]*0.001
print (cell13)
cell13_str=''+str(cell13)

#Cell_14
cell14 = (Antw33.encode('hex') [(32*2):(33*2+2)])
cell14 = struct.unpack('>H',unhexlify(cell14))[0]*0.001
print (cell14)
cell14_str=''+str(cell14)

#Cell_15
cell15 = (Antw33.encode('hex') [(34*2):(35*2+2)])
cell15 = struct.unpack('>H',unhexlify(cell15))[0]*0.001
print (cell15)
cell15_str=''+str(cell15)

#Cell_16
cell16 = (Antw33.encode('hex') [(36*2):(37*2+2)])
cell16 = struct.unpack('>H',unhexlify(cell16))[0]*0.001
print (cell16)
cell16_str=''+str(cell16)

data_power_temp = (Antw33.encode('hex') [92*2:92*2+2])
data_power_temp=int(data_power_temp,16)
print (data_power_temp)
data_power_temp_str=''+str(data_power_temp)

data_balance_temp = (Antw33.encode('hex') [94*2:94*2+2])
data_balance_temp=int(data_balance_temp,16)
print (data_balance_temp)
data_balance_temp_str=''+str(data_balance_temp)

data_cell_temp_1 = (Antw33.encode('hex') [96*2:96*2+2])
data_cell_temp_1=int(data_cell_temp_1,16)
print (data_cell_temp_1)
data_cell_temp_1_str=''+str(data_cell_temp_1)


data_cell_temp_2 = (Antw33.encode('hex') [98*2:98*2+2])
data_cell_temp_2=int(data_cell_temp_2,16)
print (data_cell_temp_2)
data_cell_temp_2_str=''+str(data_cell_temp_2)

data_Status_charge = (Antw33.encode('hex') [103*2:103*2+2])
data_Status_charge=int(data_Status_charge,16)
print (data_Status_charge)
data_Status_charge_str=''+str(data_Status_charge)

data_Status_discharge = (Antw33.encode('hex') [104*2:104*2+2])
data_Status_discharge=int(data_Status_discharge,16)
print (data_Status_discharge)
data_Status_discharge_str=''+str(data_Status_discharge)

data_Status_balance = (Antw33.encode('hex') [105*2:105*2+2])
data_Status_balance=int(data_Status_balance,16)
print (data_Status_balance)
data_Status_balance_str=''+str(data_Status_balance)

ser.close()

data = [{
    "measurement": "Klara",
    "tags": {"session": "test4"},
    "fields": {
        "remaining_ah": data_remaining_ah,
        "SoC": bms_soc,
        "Current": bms_current,
        "Battery voltage 0": bms_v,
        "Cell avg": cell_avg,
        "Cell min": cell_min,
        "Cell max": cell_max,
        "Cell voltage 0": cell1,
        "Cell voltage 1": cell2,
        "Cell voltage 2": cell3,
        "Cell voltage 3": cell4,
        "Cell voltage 4": cell5,
        "Cell voltage 5": cell6,
        "Cell voltage 6": cell7,
        "Cell voltage 7": cell8,
        "Cell voltage 8": cell9,
        "Cell voltage 9": cell10,
        "Cell voltage 10": cell11,
        "Cell voltage 11": cell12,
        "Cell voltage 12": cell13,
        "Cell voltage 13": cell14,
        "Cell voltage 14": cell15,
        "Cell voltage 15": cell16,
        "Power temperature": data_power_temp,
        "Balance temperature": data_balance_temp,
        "Cell temperature 0": data_cell_temp_1,
        "Cell temperature 1": data_cell_temp_2,
        "Status charge": data_Status_charge,
        "Status discharge": data_Status_discharge,
        "Status balance": data_Status_balance
    },
    "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
}]

write_api.write(bucket, org, data)
