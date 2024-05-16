from flask import Flask, render_template
import serial
import threading

app = Flask(__name__)

# 初始化序列通訊
ser = serial.Serial('/dev/cu.usbserial-0001', 9600, timeout=1)
data = "No data yet"
lock = threading.Lock()

def read_from_port(ser):
    global data
    while True:
        try:
            line = ser.readline().decode('utf-8').rstrip()
            if line:
                with lock:
                    data = line
        except:
            break

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/data')
def get_data():
    with lock:
        return data  # 返回當前全局變量 `data` 的值

if __name__ == '__main__':
    app.run(debug=True)
