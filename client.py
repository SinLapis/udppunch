#-*- coding:utf-8 -*-
import threading, socket, re, time

server_addr = ('54.169.131.175', 9999)

class Client():

	def __init__(self):

		self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.self_addr = None
		self.other_addr = None

	def addr_convert(self, s):

		re_addr = re.compile(r'\(\'(.*)\',\s(.*)\)')
		t = re_addr.match(s).groups()
		ip = t[0]
		port = int(t[1])
		return ip, port

	def msg_convert(self, s):

		re_msg = re.compile(r'addr:(.*)msg:(.*)')
		t = re_msg.match(s).groups()
		addr = t[0]
		msg = t[1]
		return addr, msg

	def start(self):

		while True:
			data = 'ready'
			self.sockfd.sendto(data.encode('utf-8'), server_addr)

			data, addr = self.sockfd.recvfrom(1024)
			data = data.decode('utf-8')
			if addr == server_addr:
				self.self_addr = self.addr_convert(data)
				break
		
	def request(self):

		while True:
			data = 'request'
			self.sockfd.sendto(data.encode('utf-8'), server_addr)
			data, addr = self.sockfd.recvfrom(1024)
			data = data.decode('utf-8')
			if data != 'none' and addr == server_addr:
				self.other_addr = self.addr_convert(data)
				break

	def init(self):

		n = 0
		while n > 10:
			data = 'init'
			print('init')
			self.sockfd.sendto(data.encode('utf-8'), self.other_addr)
			data, addr = self.sockfd.recvfrom(1024)
			data = data.decode('utf-8')
			if addr == self.other_addr:
				if data == 'ok':
					data = 'ok'
					self.sockfd.sendto(data.encode('utf-8'), self.other_addr)
					return True
				if data == 'init':
					data = 'ok'
					self.sockfd.sendto(data.encode('utf-8'), self.other_addr)
			n += 1
		return False

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
					print(data)

		threading.Thread(target = send, args = (self.sockfd, )).start()
		threading.Thread(target = recv, args = (self.sockfd, )).start()

	def sy_chat(self):

		def sy_send(sock):

			while True:
				data = 'addr:' + str(self.other_addr) + 'msg:' + input()
				sock.sendto(data.encode('utf-8'), server_addr)

		def sy_recv(sock):

			while True:
				data, addr = sock.recvfrom(1024)
				data = data.decode('utf-8')
				try:
					addr, msg = self.msg_convert(data)
					print('from:' + addr + '\n' + msg)
				except Exception as e:
					print('error')
					pass

		threading.Thread(target = sy_send, args = (self.sockfd, )).start()
		threading.Thread(target = sy_recv, args = (self.sockfd, )).start()


	def main(self):
		self.start()
		self.request()
		is_sy = self.init()
		print(is_sy)
		if is_sy == True:
			self.chat()
		else:
			self.sy_chat()

if __name__ == '__main__':

	c = Client()
	c.main()
		


