import socket
import struct
from PIL import Image
import io
import os


def ensure_directory(directory):
    """确保目录存在，不存在则创建。"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_next_filename(directory):
    """获取下一个递增命名的文件名，从1开始，格式为 '1.png', '2.png' ..."""
    i = 1
    while os.path.exists(os.path.join(directory, f"{i}.png")):
        i += 1
    return os.path.join(directory, f"{i}.png")


def receive_image(server_socket):
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # 接收图片大小信息
    img_size_data = conn.recv(4)
    img_size = struct.unpack('!I', img_size_data)[0]

    # 接收图片数据
    img_data = b""
    while len(img_data) < img_size:
        packet = conn.recv(4096)
        if not packet:
            break
        img_data += packet

    # 将字节数据转换为图片
    image = Image.open(io.BytesIO(img_data))

    # 确保图片保存目录存在
    base_dir = os.path.dirname(__file__)
    pictures_dir = os.path.join(base_dir, "pictures")
    ensure_directory(pictures_dir)

    # 获取递增命名的文件名并保存图片
    filename = get_next_filename(pictures_dir)
    image.save(filename)

    # 打印图片存储路径
    print(f"Image received and saved as '{filename}'")
    print(f"Full image path: {os.path.abspath(filename)}")

    conn.close()


def start_server(host='0.0.0.0', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")
        while True:
            receive_image(server_socket)


if __name__ == "__main__":
    start_server()
