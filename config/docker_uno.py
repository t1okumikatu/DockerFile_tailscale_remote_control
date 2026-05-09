import serial
import time

# ESP32を繋いだときに Ubuntuが認識するパス
# /dev/ttyUSB0 か /dev/ttyACM0 が一般的です
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 115200

try:
    # シリアルポートの初期化
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # 接続安定待ち
    print(f"Connected to ESP32 at {SERIAL_PORT}")

    while True:
        angle = input("サーボの角度を入力 (0-180) / 終了は q: ")
        
        if angle.lower() == 'q':
            break
            
        if angle.isdigit():
            # 数字に改行コードを付けて送信
            ser.write(f"{angle}\n".encode())
            print(f"Sent: {angle}")
        else:
            print("数字を入力してください")

    ser.close()
    print("Closed.")

except Exception as e:
    print(f"Error: {e}")