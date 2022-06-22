from time import sleep
import serial

ser = serial.Serial('/dev/cu.usbserial-0001', 115200)

def get_sensor_data():
    return_list = [] 
    

    ser.flushInput()
    while True:
        device_data_str = str(ser.readline())
        device_data_str = device_data_str.replace("b'", '')
        device_data_str = device_data_str.replace("\\r\\n'", '')
        device_data_str = device_data_str.split('\\')[0]
        device_data_list = device_data_str.split(' ')
        sensor_num = device_data_list[0]
        if(sensor_num == ''):
            continue
        sensor_num = int(sensor_num)
        if sensor_num != 0:
            continue
        if len(device_data_list) > 1:
            sensor_val = float(device_data_list[1])
        else:
            sensor_val = 0
        sensor_num_ind = sensor_num
        while(sensor_num_ind > 0):
            sensor_num_ind -= 1
            
        for sensor_num_ind in range(4 - sensor_num - 1):
            return_list.append(sensor_val)
            device_data_str = str(ser.readline())
            device_data_str = device_data_str.replace("b'", '')
            device_data_str = device_data_str.replace("\\r\\n'", '')
            device_data_str = device_data_str.split('\\')[0]
            device_data_list = device_data_str.split(' ')
            sensor_val = float(device_data_list[1])
        return_list.append(sensor_val)
        if len(return_list) != 4:
            continue
        break

    return return_list