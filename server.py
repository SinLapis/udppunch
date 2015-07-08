#-*- coding:utf-8 -*-
import threading, socket

class Server():
	def __init__(self):
		SERVER_PORT = 9999
		self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sockfd.bind(('',SERVER_PORT))
		self.addr_list = []
	def main(self):
		while True:
			recv_data, addr = self.sockfd.recvfrom(1024)
			recv_data = recv_data.decode('utf-8')

			if recv_data == 'ready':
				self.addr_list.append(addr)
				send_data = str(addr)
				self.sockfd.sendto(send_data.encode('utf-8'), addr)

			if recv_data == 'request' and len(self.addr_list) > 1:
				n = self.addr_list.index(addr)
				target_addr = self.addr_list[1-n]
				send_data = str(target_addr)
				self.sockfd.sendto(send_data.encode('utf-8'), addr)

			if recv_data == 'request' and len(self.addr_list) <= 1:
				send_data = 'none'
				self.sockfd.sendto(send_data.encode('utf-8'), addr)

if __name__ == '__main__':
	s = Server()
	s.main()

