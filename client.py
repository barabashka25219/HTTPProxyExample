import socket

class Client:
	def __init__(self, serv_addr, serv_port):
		self.serv_addr = serv_addr
		self.serv_port = serv_port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect_to_server(self):
		try:
			self.sock.connect((self.serv_addr, self.serv_port))

		except:
			print("[*] Can't connect to proxy.")
			return None

		print(f"[*] Connected to {self.serv_addr}:{self.serv_port}")

	def get_user_request(self):
		self.request = input('[*] Enter web resource for HTTP GET request: ')

		if not len(self.request):
			return None

	def send_request(self):
		try:
			self.sock.send(self.request.encode())
			return self.request

		except:
			print(f"[!] Can't send your request {self.request}")
			return None


	def receive_reply(self):
		self.sock.settimeout(2)

		try:
			self.reply = self.sock.recv(4096).decode()

			if self.reply == "Wrong":
				print(f"Can't connect to {self.request}. Does this resource exist?\n")

		except:
			print("[!] Time out is up")
			return None

		return self.reply
			

client = Client('127.0.0.1', 5555)

client.get_user_request()
client.connect_to_server()
client.send_request()

reply = client.receive_reply()

print(reply)
