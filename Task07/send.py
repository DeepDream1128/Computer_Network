import socket

def send_file_ipv6(filename, target_ip, port):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((target_ip, port))

    # 发送文件名
    filename_bytes = filename.encode('utf-8')
    filename_length = len(filename_bytes)
    s.sendall(filename_length.to_bytes(4, 'big'))  # 发送文件名长度（4字节）
    s.sendall(filename_bytes)  # 发送文件名

    # 发送文件数据
    with open(filename, 'rb') as f:
        print("发送数据中...")
        while True:
            data = f.read(65536)
            if not data:
                break
            s.send(data)

    print("文件发送完毕")
    s.close()


send_file_ipv6('Task07/yolov5s.pt', '2001:da8:8008:315:b9b4:aa92:96c4:5fee', 12345)