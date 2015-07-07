#-*- coding:utf-8 -*-
import threading, socket, re

server_addr = ('127.0.0.1', 9999)

class Client():

	def __init__(self):

		self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.self_addr = None

	def addr_convert(self, s):

		re_addr = re.compile(r'\(\'(.*)\',\s(.*)\)')
		t = re_addr.match(s).groups()
		s1 = t[0]
		s2 = int(t[1])
		return s1, s2

	def start(self):

		data = 'ready'
		self.sockfd.sendto(data.encode('utf-8'), server_addr)

		data, addr = self.sockfd.recvfrom(1024)
		data = data.decode('utf-8')
		self.self_addr = self.addr_convert(data)


	def main(self):
		self.start()

if __name__ == '__main__':

	c = Client()
	c.main()
		


