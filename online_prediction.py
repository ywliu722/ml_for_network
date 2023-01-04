import sys
import joblib
import paho.mqtt.client as mqtt
from sklearn.tree import DecisionTreeClassifier
import json

MQTT_PORT = 1883

SEC_TO_US = 1000000
BYTE_TO_BITS = 8
BITS_TO_MEGA = 1024 * 1024

OUTPUT_PATH = '/home/yw/final/CS_Project-Linux_Trinus/test.json'
MODEL_PATH = 'pre-trained_model'

clf = joblib.load(MODEL_PATH)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("TESTING")

def on_message(client, userdata, msg):
    # record the other device airtime
    other_device_airtime_per = 0.0  # in percentage
    print("HEHEHE")
    # parsing the received message
    input = msg.payload.decode().split()
    nss = input[0]
    mcs_index = input[1]
    guard_interval = input[2]
    data_len = float(input[3])      # in bytes
    interval = float(input[4])      # in second
    tx_airtime = float(input[5])    # in micro-second

    # parsing GI
    GI_in_num = 0
    if(guard_interval == "SGI"):
        GI_in_num = 1
    else:
        GI_in_num = 0

    throughput = (data_len * BYTE_TO_BITS) / BITS_TO_MEGA   # in Mbps
    airtime_per = tx_airtime / (interval * SEC_TO_US)       # in percentage

    # parsing other device's airtime
    for i in range(6,len(input),2):
        current_device_airtime_per = float(input[i+1]) / (interval * SEC_TO_US)
        # check the value is correct or not
        if current_device_airtime_per < 0 or current_device_airtime_per > 1:
            continue

        # sum up the total used airtime
        other_device_airtime_per += current_device_airtime_per


    x_test = [[int(nss[3]), int(mcs_index[3]), GI_in_num, airtime_per, other_device_airtime_per]]
    y_predict = clf.predict(x_test)
    print(y_predict)

    if y_predict == 0:
        video_quality = "1080p"
    elif y_predict == 1:
        video_quality = "900p"
    elif y_predict == 2:
        video_quality = "720p"
    elif y_predict == 3:
        video_quality = "540p"
    else:
        video_quality = "360p"

    output = {
        "quality" : video_quality
    }

    # output the current state to stdout
    print(output)
    print(f'{nss} {mcs_index} {guard_interval}')
    print(f'Throughput: {throughput} Mbps')
    print(f'Airtime: {airtime_per}')
    print(f'Other Device: {other_device_airtime_per}')
    print("-----------------------------------------------")

    # output the quality
    try:
        input_file = open (OUTPUT_PATH,'r')
        json_array = json.load(input_file)
        input_file.close()
        current_quality = json_array['quality']
        if current_quality != video_quality:
            output_file = open(OUTPUT_PATH,"w")
            json.dump(output, output_file)
            output_file.close()
    except:
        pass

def main():
    if len(sys.argv) != 2:
        print(f'Usage: $ python3 {sys.argv[0]} <broker IP>')
        return

    brokerIP = sys.argv[1]
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(brokerIP, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == '__main__':
    main() 