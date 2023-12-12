import time
import socket

# 参数初始化
alpha = 0.125
beta = 0.25
G = 0.1  # 100毫秒

# 初始RTT、SRTT、RTTVAR和RTO的设定
initial_rtt = 0.5  # 假设的初始RTT值，单位秒
srtt = initial_rtt
rttvar = initial_rtt / 2
rto = srtt + max(G, 4 * rttvar)

# 创建TCP连接
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("www.google.com", 80))  # 连接到目标服务器和端口

# 发送和接收数据，计算RTT
try:
    for _ in range(5):  # 发送五次数据进行测试
        send_time = time.time()
        client_socket.sendall(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
        response = client_socket.recv(4096)
        recv_time = time.time()

        # 计算当前RTT
        rtt = recv_time - send_time

        # 更新SRTT和RTTVAR
        rttvar = (1 - beta) * rttvar + beta * abs(srtt - rtt)
        srtt = (1 - alpha) * srtt + alpha * rtt

        # 更新RTO
        rto = srtt + max(G, 4 * rttvar)

        print(f"RTT: {rtt:.3f}, SRTT: {srtt:.3f}, RTTVAR: {rttvar:.3f}, RTO: {rto:.3f}")

finally:
    client_socket.close()
