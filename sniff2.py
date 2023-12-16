from scapy.all import sniff, IP
import struct

def checksum(ip_header):
    """
    计算 IP 首部的检验和
    """
    sum = 0
    # 每次取两个字节
    for i in range(0, len(ip_header), 2):
        word = (ip_header[i] << 8) + (ip_header[i + 1] if i+1 < len(ip_header) else 0)
        sum += word
        sum = (sum & 0xffff) + (sum >> 16)  # 将溢出的部分加到低16位

    return ~sum & 0xffff

def handle_packet(packet):
    """
    处理捕获的 IP 数据报
    """
    if IP in packet:
        ip_header = packet[IP]
        print(f"捕获到 IP 数据报：{ip_header.summary()}")

        # 获取原始的 IP 首部信息
        raw_header = bytes(ip_header)[:20]  # 只取 IP 首部前20字节
        print(f"原始首部信息：{raw_header}")

        # 计算并显示检验和
        calculated_checksum = checksum(raw_header)
        print(f"计算的检验和：{calculated_checksum:04x}")

# 嗅探网络上的 IP 数据报
sniff(filter="ip", prn=handle_packet, count=10)
