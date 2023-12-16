import socket
import time

def receive_file_ipv6(port):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(('::', port))
    s.listen(5)
    print(f"服务器启动，监听端口 {port}...")

    conn, addr = s.accept()
    print(f"来自 {addr} 的连接已建立")

    # 接收文件名
    filename_length_bytes = conn.recv(4)
    filename_length = int.from_bytes(filename_length_bytes, 'big')
    filename_bytes = conn.recv(filename_length)
    filename = filename_bytes.decode('utf-8')
    print(f"接收文件名: {filename}")

    # 接收文件数据
    with open(filename, 'wb') as f:
        print("接收数据中...")
        total_bytes_received = 0
        start_time = time.time()
        while True:
            data = conn.recv(65536)
            if not data:
                break
            bytes_received = len(data)
            total_bytes_received += bytes_received
            f.write(data)

            # 计算每秒的接收速度
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 0:
                speed = total_bytes_received / elapsed_time / (1024 * 1024)
                print(f"\r当前接收速度: {speed:.2f} Mb/秒", end='', flush=True)

    print("\n文件接收完毕")
    conn.close()
    s.close()

receive_file_ipv6(12345)
