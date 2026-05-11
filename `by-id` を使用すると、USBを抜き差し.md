`by-id` を使用すると、USBを抜き差ししたり他のデバイスを繋いだりした際に `/dev/ttyUSB0` が `ttyUSB1` にズレる問題を回避できるため、非常に賢明な選択です。

先ほどのログにあった **2WD用のFTDIチップ** のIDを参考に、`docker-compose.yaml` への追記見本を作成しました。

### `docker-compose.yaml` の追記見本

`services` 内の `robot-app`（または `robot-control`）の項目に、以下のように `devices` セクションを追加してください。

```yaml
services:
  robot-app:
    image: python:3.11-slim
    # ... 他の設定 ...
    devices:
      # 左車輪用 (by-idで指定)
      - "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B0001KJH-if00-port0:/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B0001KJH-if00-port0"
      # 右車輪用 (by-idで指定)
      - "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B003725S-if00-port0:/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B003725S-if00-port0"
      # 【重要】ここにKeigan MotorのIDを追記します
      - "/dev/serial/by-id/[ここにKeiganMotorのID]:/dev/serial/by-id/[ここにKeiganMotor의ID]"
    
    privileged: true  # 確実にシリアル通信を通すために推奨
    user: root        # 権限問題を避けるためにrootで実行

```

---

### 手順：Keigan MotorのIDを確認する方法

Keigan Motorの正確なIDを調べるために、ホスト側（Ubuntu/WSL2）のターミナルで以下のコマンドを打ってください。

```bash
ls /dev/serial/by-id/

```

実行すると、以下のような名前のリストが出てきます。
`usb-Keigan_KeiganMotor_KM-1_...-if00`

この名前をコピーして、上記の YAML の `[ここにKeiganMotorのID]` の部分に貼り付けてください。

---

### 設定を反映させる

YAMLを書き換えて保存したら、以下のコマンドで反映させます。

```bash
# 一度完全に削除して、新しいデバイス設定で作り直す
docker compose down
docker compose up -d

```

### 動作確認のコツ

コンテナが起動した後、以下のコマンドでコンテナ内からデバイスが見えているか最終確認できます。

```bash
docker compose exec robot-app ls /dev/serial/by-id/

```

ここにリストが表示されれば、`integrated_server_v9.py` 内のプログラムから Keigan Motor にアクセスできるようになります！