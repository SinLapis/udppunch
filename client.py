#-*- coding:utf-8 -*-
import threading, socket, re

server_addr = ('127.0.0.1', 9999)

class Client():

	def __init__(self):

		self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.self_addr = None
		self.other_addr = None

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
		
	def request(self):
		while True:
			data = 'request'
			self.sockfd.sendto(data.encode('utf-8'), server_addr)
			data, addr = self.sockfd.recvfrom(1024)
			data = data.decode('utf-8')
			if data != 'none':
				self.other_addr = self.addr_convert(data)
				break

	def init(self):

		m = n = 0
		while True:
			data = 'init'
			self.sockfd.sendto(data.encode('utf-8'), self.other_addr)
			data, addr = self.sockfd.recvfrom(1024)
			data = data.decode('utf-8')
			if data == 'ok':
				m = 1
			if data == 'init':
				data = 'ok'
				self.sockfd.sendto(data.encode('utf-8'), self.other_addr)
				n = 1
			if m + n == 1:
				return True

	def chat(self):

		def send(sock):

			while True:
				data = input()
				sock.sendto(data.encode('utf-8'), self.other_addr)

		def recv(sock):

			while True:
				data, addr = sock.recvfrom(1024)
				if addr == self.other_addr:
					data = data.decode('utf-8')
					print('Recevide from %s:%s' % addr)
					print(data)

		threading.Thread(target = send, args = (self.sockfd, )).start()
		threading.Thread(target = recv, args = (self.sockfd, )).start()



	def main(self):
		self.start()
		self.request()
		self.init()
		self.chat()

if __name__ == '__main__':

	c = Client()
	c.main()
		


