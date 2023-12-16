from scapy.all import *
import time

def tcp_handshake(target_ip, target_port):
    # 构造IPv4 SYN报文
    ip = IP(dst=target_ip)
    syn = TCP(sport=RandShort(), dport=target_port, flags="S")
    syn_ack = sr1(ip/syn, timeout=1)

    # 检查是否收到IPv6 SYN-ACK响应
    if syn_ack and syn_ack.haslayer(TCP) and syn_ack.getlayer(TCP).flags & 0x12:
        # 发送IPv6 ACK报文
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
    fin = TCP(sport=RandShort(), dport=target_port, flags="FA", seq=seq, ack=ack_seq)
    send(ip/fin)

    # 接收服务器响应并丢弃RST报文
    ans, _ = sr(ip/TCP(sport=fin.dport, dport=fin.sport, flags="A"), timeout=1, verbose=False)
    
    if ans and ans[0][1].haslayer(TCP):
        tcp_layer = ans[0][1].getlayer(TCP)
        if tcp_layer.flags & 0x04:  # 检查是否是 RST
            print("收到RST，但已丢弃")
        else:
            print("未收到RST")

    # 发送最后的ACK报文
    last_ack = TCP(sport=fin.sport, dport=target_port, flags="A", seq=tcp_layer.ack, ack=tcp_layer.seq + 1)
    send(ip/last_ack)
    print("TCP四次挥手完成")

if __name__ == "__main__":
    target_ip = "10.206.17.20"  # 目标IPv6服务器IP地址
    target_port = 7890  # 目标服务器端口
    seq, ack_seq = tcp_handshake(target_ip, target_port)

    if seq and ack_seq:
        time.sleep(2)  # 等待一段时间再开始挥手
        tcp_teardown(target_ip, target_port, seq, ack_seq)
