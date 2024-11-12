import socket
import struct
from PIL import ImageGrab
import io
import keyboard

def capture_screen():
    # 截屏并将其转换为字节数据
    screenshot = ImageGrab.grab()
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
    server_ip = '192.168.1.20'  # 替换为服务器的IP地址
    port = 5000

    print("Press 'P' to capture and send screenshot.")

    # 等待用户按下 'P' 键
    while True:
        if keyboard.is_pressed("p"):
            print("Capturing and sending screenshot...")
            img_data = capture_screen()
            send_image(img_data, server_ip, port)
            print("Waiting for next 'P' key press...")
            # 等待 'P' 键松开，防止多次触发
            while keyboard.is_pressed("p"):
                pass
