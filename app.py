from flask import Flask, render_template, jsonify
import serial
import threading

# 創建 Flask 應用實例
app = Flask(__name__)

# 初始化序列通訊，設置連接到特定USB串行埠和波特率
ser = serial.Serial('COM3', 9600, timeout=1)
weight = "No data yet"  # 初始化重量數據為 "No data yet"
lock = threading.Lock()  # 創建一個鎖，用於線程間的同步

def read_from_port(ser):
    global weight  # 引用全局變量 weight
    while True:
        try:
            line = ser.readline().decode('utf-8').rstrip()  # 從串列埠讀取一行數據並解碼
            if line:  # 如果有數據讀入
                with lock:  # 線程安全地更新重量數據
                    weight = line
                    temp_weight = float(line)
                    weight = 0 if temp_weight == 0 else temp_weight
        except:
            break  # 如果發生錯誤，退出循環

# 在另一個線程中啟動讀取數據的函數
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

# 定義路由，當訪問網站根目錄 '/' 時觸發
@app.route('/')
def index():
    # 返回 index.html 頁面
    return render_template('index.html')

# 定義 API 路由，用於返回當前重量數據的 JSON
@app.route('/weight')
def get_weight():
    with lock:  # 線程安全地訪問全局變量 weight
        return jsonify({'weight': weight})

# 啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)  # 啟動服務器，開啟調試模式
