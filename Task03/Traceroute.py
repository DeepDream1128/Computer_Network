from scapy.all import *
import sys

def traceroute(dest, max_hops=30):
    for ttl in range(1, max_hops + 1):
        pkt = IP(dst=dest, ttl=ttl) / ICMP()
        # 获取当前时间戳
        start_time = time.time()
        # 发送数据包并等待响应
        reply = sr1(pkt, verbose=0, timeout=2)
        # 计算往返时延
        rtt = time.time() - start_time

        if reply is None:
            print(f"{ttl}\t*\t*")
        else:
            print(f"{ttl}\t{reply.src}\t{rtt:.3f} ms")
            if reply.type == 0:  # ICMP Echo Reply
                print("到达目标")
                break

if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "google.com"
    traceroute(dest)
