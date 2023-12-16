import socket

def start_server(port):
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind(('::', port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        
        print(f"Accepted connection from {addr}")

        # 输出信息
        print("Received handshake request, sending RST packet")

        # 发送RST包
        client_socket.close()

if __name__ == "__main__":
    start_server(12345)
