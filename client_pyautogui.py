import socket
import struct
import pyautogui  # 使用 pyautogui 来进行截图
import io
import time

def capture_screen():
    # 使用 pyautogui 截屏并将其转换为字节数据
    screenshot = pyautogui.screenshot()
    with io.BytesIO() as output:
        screenshot.save(output, format="PNG")
        img_data = output.getvalue()
    return img_data

def send_image(img_data, server_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))

        # 发送图片大小信息
        img_size = len(img_data)
        client_socket.sendall(struct.pack('!I', img_size))

        # 发送图片数据
        client_socket.sendall(img_data)
        print("Image sent successfully.")

if __name__ == "__main__":
    server_ip = '192.168.1.39'  # 替换为服务器的IP地址
    port = 5000

    print("Program started. Capturing and sending screenshots every 5 seconds.")

    # 程序启动后每5秒自动截图一次
    while True:
        img_data = capture_screen()
        send_image(img_data, server_ip, port)
        time.sleep(3)  # 每5秒截图一次
