from scapy.all import *
import time 

def tcp_handshake(target_ip, target_port):
    # 构造SYN报文
    ip = IP(dst=target_ip)
    syn = TCP(sport=RandShort(), dport=target_port, flags="S")
    syn_ack = sr1(ip/syn, timeout=1)

    # 检查是否收到SYN-ACK响应
    if syn_ack and syn_ack.haslayer(TCP) and syn_ack.getlayer(TCP).flags & 0x12:
        # 发送ACK报文
        ack = TCP(sport=syn.sport, dport=target_port, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
        send(ip/ack)
        print("TCP三次握手完成")
        return syn_ack.seq + 1, ack.seq
    else:
        print("握手失败")
        return None, None

def tcp_teardown(target_ip, target_port, seq, ack_seq):
    # 发送FIN报文
    ip = IP(dst=target_ip)
    fin = TCP(sport=RandShort(), dport=target_port, flags="FA", seq=ack_seq, ack=seq)
    fin_ack = sr1(ip/fin, timeout=1)

    # 检查是否收到FIN-ACK响应
    if fin_ack and fin_ack.haslayer(TCP) and fin_ack.getlayer(TCP).flags & 0x11:
        # 发送最后的ACK报文
        last_ack = TCP(sport=fin.sport, dport=target_port, flags="A", seq=fin_ack.ack, ack=fin_ack.seq + 1)
        send(ip/last_ack)
        print("TCP四次挥手完成")

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # 目标服务器IP
    target_port = 8080              # 目标服务器端口
    seq, ack_seq = tcp_handshake(target_ip, target_port)

    if seq and ack_seq:
        time.sleep(2)  # 等待一段时间再开始挥手
        tcp_teardown(target_ip, target_port, seq, ack_seq)
