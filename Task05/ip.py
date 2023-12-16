from scapy.all import *
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        # TCP SYN Scan
        syn_pkt = IP(dst=ip) / TCP(dport=port, flags="S")
        response = sr1(syn_pkt, timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response.getlayer(TCP).flags & 0x12:
            return port, 'Open'

        # UDP Scan
        udp_pkt = IP(dst=ip) / UDP(dport=port)
        response = sr1(udp_pkt, timeout=1, verbose=0)
        if not response or (response.haslayer(ICMP) and response.getlayer(ICMP).type != 3):
            return port, 'Open/Filtered'
    except Exception as e:
        return port, 'Error'
    return port, 'Closed'

def scan(ip, ports, max_threads=100):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        scan_results = executor.map(lambda p: scan_port(ip, p), ports)
        for port, status in scan_results:
            print(f"Port {port}: {status}")

if __name__ == "__main__":
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "10.206.17.20"
    ports = range(1, 124)  # Standard range of ports
    scan(target_ip, ports)
