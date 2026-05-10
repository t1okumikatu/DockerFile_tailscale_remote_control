import pygame
import requests
import time

# 設定
R_HOST = '100.101.141.2'
#R_HOST = '100.124.195.2'
URL = f'http://{R_HOST}:5000/control' # FlaskのURL

def start_joy_client():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("ジョイスティックが見つかりません")
        return

    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"使用中: {joy.get_name()}")

    try:
        while True:
            pygame.event.pump()
            
            # スティック値取得 (-1.0 ～ 1.0)
            axis_x = joy.get_axis(0)
            axis_y = joy.get_axis(1)

            # デッドゾーン処理
            if abs(axis_x) < 0.1: axis_x = 0.0
            if abs(axis_y) < 0.1: axis_y = 0.0

            # 指揮値計算 (例: 最大500 RPM)
            speed = -axis_y * 500
            turn = axis_x * 200
            
            payload = {
                "left": speed + turn,
                "right": speed - turn
            }

            try:
                # HTTP POSTで送信。タイムアウトを0.5秒に設定
                res = requests.post(URL, json=payload, timeout=0.5)
                print(f"送信中 L:{payload['left']:>4.0f} R:{payload['right']:>4.0f} | Status: {res.status_code}")
            except Exception as e:
                print(f"通信エラー: {e}")

            time.sleep(0.1) # 10Hz

    except KeyboardInterrupt:
        print("終了します")
    finally:
        pygame.quit()

if __name__ == "__main__":
    start_joy_client()