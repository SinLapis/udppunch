#-*- coding:utf-8 -*-
import threading, socket, re

class Server():

	#初始化服务器参数，实例化socket
	def __init__(self):

		SERVER_PORT = 9999
		self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sockfd.bind(('',SERVER_PORT))
		self.addr_list = []

	#从字符串中提取地址并转换成元组
	def addr_convert(self, s):

		re_addr = re.compile(r'\(\'(.*)\',\s(.*)\)')
		t = re_addr.match(s).groups()
		ip = t[0]
		port = int(t[1])
		return ip, port

	#提取地址和聊天信息
	def msg_convert(self, s):

		re_msg = re.compile(r'addr:(.*)msg:(.*)')
		t = re_msg.match(s).groups()
		addr = t[0]
		msg = t[1]
		return addr, msg

	#主函数，根据客户端发来的不同信息进行处理
	def main(self):

		while True:
			recv_data, src_addr = self.sockfd.recvfrom(1024)
			recv_data = recv_data.decode('utf-8')

			if recv_data == 'ready':
				self.addr_list.append(src_addr)
				send_data = str(src_addr)
				self.sockfd.sendto(send_data.encode('utf-8'), src_addr)
				print('list update: %s is added to list' % send_data)

			elif recv_data == 'close':
				self.addr_list.remove(str(src_addr))

			elif recv_data == 'request' and len(self.addr_list) == 2:
				n = self.addr_list.index(src_addr)
				target_addr = self.addr_list[1-n]
				send_data = str(target_addr)
				self.sockfd.sendto(send_data.encode('utf-8'), src_addr)
				print('send %s to %s' % (send_data, str(src_addr)))

			elif recv_data == 'request' and len(self.addr_list) <= 1:
				send_data = 'none'
				self.sockfd.sendto(send_data.encode('utf-8'), src_addr)

			else:
				try:
					addr, msg = self.msg_convert(recv_data)
					target_addr = self.addr_convert(addr)
					data = 'addr:' + addr + 'msg:' + msg
					self.sockfd.sendto(data.encode('utf-8'), target_addr)
					print('relay message from %s to %s' % (str(src_addr), str(target_addr)))
				except Exception as e:
					print('error')
					pass


if __name__ == '__main__':
	s = Server()
	s.main()