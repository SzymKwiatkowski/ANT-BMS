from binascii import unhexlify, hexlify
import bluetooth as bt
from datetime import datetime
import json  # only for pretty dictionary printing
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# ======================================================================================================================
# global parameters
# ======================================================================================================================
# bluetooth connection
serverMACAddress = '20:A1:11:01:23:45'
port = 1
protocol = bt.RFCOMM

# influxdb
url = "your url link for uploading data"
token = "put_your_api_token_here"
measurement = "Klara"
org = "Test"
bucket = "Pomiary"
session = "test4"

# BMS start codes
test_code_1 = '5A5A5A00005A'
test_code_2 = 'DBDB00000000'

cell_num = 16  # number of cell connected to BMS - value copied from original script

# Connection objects - initialize them with connect() function
ser = bt.BluetoothSocket()
client = InfluxDBClient(url=url)
write_api = client.write_api()


# ======================================================================================================================
# connection
# ======================================================================================================================
def connect() -> None:
    """
    Creates bluetooth socket and tries to connect to mac address on port set in parameters section.

    Creates influxdb client and write_api for easier usage. All parameters used are set in parameters section.
    If if client cannot connect to server, raises exception.
    """
    global ser, client, write_api
    # Bluetooth connection
    try:
        ser = bt.BluetoothSocket(protocol)
        ser.connect((serverMACAddress, port))
    except OSError:
        raise Exception("Cannot connect to BMS via Bluetooth")

    # Influxdb database connection
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    if not client.ping():
        raise Exception("Cannot connect to server")


# ======================================================================================================================
# Read data from BMS
# ======================================================================================================================
def read_data() -> dict:
    """
    Sends two start codes to BMS and read 140 bytes. Next decodes bms data like in previous script.

    :return: Dictionary with name(str) : value(int or float) pairs.
    """
    try:
        ser.send(unhexlify(test_code_1))
        time.sleep(0.005)
        ser.send(unhexlify(test_code_2))
        time.sleep(0.01)
    except bt.BluetoothError:
        print("Exception during sending start codes")
        ser.close()

    time.sleep(1)
    antw33_bytes = ser.recv(140)
    if antw33_bytes == b'':
        print("Timeout during recv")
        return dict()

    # odpowiednik encode("hex") z python 2
    antw33 = hexlify(antw33_bytes)
    data = dict()

    # Remaining Ah =====================================================================================================
    try:
        # python will convert int to float during multiplication instead of direct conversion - easier to do
        data_remaining_ah = int(antw33[79*2:82*2+2], 16) * 0.000001
        data["remaining_ah"] = data_remaining_ah

    except TypeError or ValueError:
        print("TypeError or ValueError during remaining ah conversion")

    # SoC ==============================================================================================================
    bms_soc = int(antw33[(74*2):(75*2)], 16)
    data["SoC"] = bms_soc

    # Power ============================================================================================================
    try:
        bms_pow = int(antw33[(111 * 2):(114 * 2 + 2)], 16)
        if bms_pow > 2147483648:
            bms_pow = -(2*2147483648) + bms_pow

        bms_pow = (bms_pow * -1)
        data["Power"] = bms_pow

    except ValueError:
        pass

    # BMS current ======================================================================================================
    try:
        bms_current = int(antw33[(70 * 2):(73 * 2 + 2)], 16)
        if bms_current > 2147483648:
            bms_current = (-(2*2147483648) + bms_current) * 0.1
        else:
            bms_current = bms_current * 0.1

        bms_current = (bms_current * -1)
        data["Current"] = bms_current

    except ValueError:
        pass

    # BMS V ============================================================================================================
    bms_v = int(antw33[8:12], 16) * 0.1
    data["Battery voltage"] = bms_v

    # Cell_avg =========================================================================================================
    cell_avg = int(antw33[(121*2):(122*2+2)], 16) * 0.001
    data["Cell average"] = cell_avg

    # Cell_min =========================================================================================================
    cell_min = int(antw33[(119*2):(120*2+2)], 16) * 0.001
    data["Cell minimum"] = cell_min

    # Cell_max =========================================================================================================
    cell_max = int(antw33[(116*2):(117*2+2)], 16) * 0.001
    data["Cell maximum"] = cell_max

    # Cell voltages ====================================================================================================
    for i in range(0, cell_num*2, 2):
        cell_v = int(antw33[((6+i)*2):((7+i)*2+2)], 16) * 0.001
        data[f"Cell voltage {i/2}"] = cell_v

    # Power temperature ================================================================================================
    data_power_temp = int(antw33[92*2:92*2+2], 16)
    data["Power temperature"] = data_power_temp

    # Balance temperature ==============================================================================================
    data_balance_temp = int(antw33[94*2:94*2+2], 16)
    data["Balance temperature"] = data_balance_temp

    # Cell temperature 1 ===============================================================================================
    data_cell_temp_1 = int(antw33[96*2:96*2+2], 16)
    data["Cell temperature 0"] = data_cell_temp_1

    # Cell temperature 2 ===============================================================================================
    data_cell_temp_2 = int(antw33[98*2:98*2+2], 16)
    data["Cell temperature 1"] = data_cell_temp_2

    # Status charge ====================================================================================================
    data_status_charge = int(antw33[103*2:103*2+2], 16)
    data["Status charge"] = data_status_charge

    # Status discharge =================================================================================================
    data_status_discharge = int(antw33[104*2:104*2+2], 16)
    data["Status discharge"] = data_status_discharge

    # Status balance ===================================================================================================
    data_status_balance = int(antw33[105*2:105*2+2], 16)
    data["Status balance"] = data_status_balance

    return data


# ======================================================================================================================
# Printing and sending data to server
# ======================================================================================================================
def pprint_data(data: dict):
    """
    Prints data dictionary in pretty way using json
    """
    print(json.dumps(data, indent=4))


def send_data(data: dict):
    """
    Converts data dictionary to format accepted by influxdb and sends it to server with globally set client
    """
    global write_api

    if write_api is None:
        print("Influxdb client was not initialized")
        return

    # converting data to influxdb format
    data_influx = {
        "measurement": measurement,
        "tags": {"session": session},  # if you dont want to set tags leave this dict empty
        "fields": data,
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    write_api.write(bucket, org, data_influx)


if __name__ == "__main__":
    connect()
    new_data = read_data()
    pprint_data(new_data)
    send_data(new_data)
