import serial

# 初始化序列通訊（根據實際情況修改端口號，例如 'COM3' 或 '/dev/ttyUSB0'）
ser = serial.Serial('/dev/cu.usbserial-0001', 9600, timeout=1)

while True:
    try:
        # 從Arduino讀取資料
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            print("Received from Arduino: ", line)
    except KeyboardInterrupt:
        print("Program interrupted by user")
        break

ser.close()