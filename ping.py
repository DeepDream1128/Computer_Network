from scapy.all import *

def ping1(sip, dip, ttl):
	'''
	发送一个 ICMP 回送请求报文
	'''

	# 构造一个IP数据报，封装 ICMP 回送请求报文
	pkt_icmp = IP(src = sip, dst = dip, ttl = ttl)/ICMP(type = 8, code = 0)
	
	try:
		# 发送一个 ICMP 回送请求报文
		# 注意 ans, 和 uans 的含义，这是重点内容
		ans, uans = sr(pkt_icmp,  timeout = 2,  verbose = False)

		# 输出调试信息：ICMP 报文中的 type 和 code
		print(ans[0][1][ICMP].type, ans[0][1][ICMP].code)

		# 超时错误
		if ans[0][1][ICMP].type == 11 and ans[0][1][ICMP].code == 0:
			print("{}: 超时错误: ".format(ans[0][1][IP].src))
		# 目的主机响应了回送请求报文，通了
		elif ans[0][1][ICMP].type == 0 and ans[0][1][ICMP].code == 0:
			print("通了: {}".format(ans[0][1][IP].src))

	except Exception as e:		# 目的主机不可达
		print('请求超时：目标主机 {} 不可达.'.format(dip))

if __name__ == '__main__':
	
	# 以下这些参数，将采用图形化界面输入
	sip = '127.0.0.1'			# 调试用的源IP地址
	#dip = '121.14.77.201'		# 调试目标主机可达的情况
	dip = 'www.baidu.com'		# 调试目标主机不可达的情况
	ttl = 64					# 调试超时错误情况
	
	ping1(sip, dip, ttl)
