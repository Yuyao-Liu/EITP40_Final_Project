import serial
import csv
from datetime import datetime

# 配置串口参数
SERIAL_PORT = "COM5"  # 根据实际串口号修改
BAUD_RATE = 9600      # 波特率，与 Arduino 代码一致
OUTPUT_FILE = "0.csv"  # 输出的 CSV 文件名

# aX,aY,aZ,gX,gY,gZ
# -0.163,0.246,2.188,190.918,-218.323,29.785
# -0.180,0.307,2.031,195.618,-178.345,19.592
# -0.276,0.314,1.834,194.031,-150.574,7.019
# -0.354,0.289,1.634,183.594,-134.583,-3.418

def main():
    try:
        # 打开串口
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT}")
            # 打开 CSV 文件
            with open(OUTPUT_FILE, mode="w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                # # 写入 CSV 表头
                # csv_writer.writerow(["aX", "aY", "aZ", "gX", "gY", "gZ", "timestamp"])
                
                # 循环读取数据
                while True:
                    try:
                        # 从串口读取一行数据
                        line = ser.readline().decode("utf-8").strip()
                        if line:
                            # 解析数据
                            data = line.split(",")
                            if len(data) == 6:  # 确保是有效数据
                                # 添加时间戳
                                # data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                # 写入 CSV
                                csv_writer.writerow(data)
                                print(data)  # 输出到控制台，便于调试
                    except KeyboardInterrupt:
                        print("\nStopping...")
                        break
    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()