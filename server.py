import socket

class Server:
	def __init__(self, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.sock.bind(('0.0.0.0', int(port)))
		print(f"[*] Listening connections on {port}")

	def listen_connections(self):
		self.sock.listen(1)

		# Принимаем по одному соединению за итерацию
		while True:
			self.client_sock, self.client_addr = self.sock.accept()
			print(f"Got connection from {self.client_addr[0]}:{self.client_addr[1]}")

			self.proxy_handler()


	def proxy_handler(self):
		while True:
			# Revceive web resource name from client
			self.received_data = self.client_sock.recv(4096).decode().rstrip()

			# Open a socket for a remote connection
			self.remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# Connect to the web resource and send GET request from our server
			try:
				self.remote_sock.connect((str(self.received_data), 80))

			except: 
				# If connection is wrong, send message to the client
				self.client_sock.send("Wrong".encode())
				break

			# Send GET HTTP request from our server 
			self.remote_sock.send(f"GET / HTTP/1.1\r\nHost: {self.received_data}\r\n\r\n".encode())

			# Wait for answer from the web resource for 2 seconds
			self.remote_sock.settimeout(2)


			while True:
				try:
					self.remote_buffer = self.remote_sock.recv(4096).decode()

					self.local_buffer = self.remote_buffer
					sent = self.client_sock.send(self.local_buffer.encode())

					print(f"[*] Sent {len(sent)} bytes to {self.client_addr[0]}")

				except:
					self.remote_sock.close()
					self.client_sock.close()
					break

			return

server = Server('5555')
server.listen_connections()