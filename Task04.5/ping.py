import os
import socket
import struct
import time
import select

def checksum(source_string):
    """
    计算校验和
    """
    sum = 0
    max_count = (len(source_string)/2)*2
    count = 0
    while count < max_count:
        val = source_string[count + 1]*256 + source_string[count]
        sum = sum + val
        sum = sum & 0xffffffff 
        count = count + 2
     
    if max_count < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff 
    
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id):
    """
    创建 ICMP Echo 请求包
    """
    header = struct.pack('bbHHh', 8, 0, 0, id, 1)
    data = 192 * b'Q'
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', 8, 0, socket.htons(my_checksum), id, 1)
    return header + data

def ping(host, timeout=1, count=4):
    """
    发送 ping 请求
    """
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"无法解析主机: {host}")
        return

    print(f"Pinging {host} [{dest_addr}] with {count} packets of data:")

    for i in range(count):
        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as e:
            print(f"无法创建 socket: {e}")
            return

        packet_id = os.getpid() & 0xFFFF
        packet = create_packet(packet_id)

        try:
            sock.sendto(packet, (dest_addr, 1))
            start_time = time.time()
            ready = select.select([sock], [], [], timeout)
            if ready[0] == []:
                print("请求超时")
            else:
                received_packet, addr = sock.recvfrom(1024)
                time_received = time.time()
                rtt = (time_received - start_time) * 1000
                print(f"来自 {addr[0]}: 字节={len(received_packet)} 时间={round(rtt, 2)}ms")
        except socket.error as e:
            print(f"发送或接收数据时发生错误: {e}")
        finally:
            sock.close()
        time.sleep(1)

if __name__ == "__main__":
    ping("www.baidu.com")
