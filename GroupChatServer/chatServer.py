'''
This file is the chat server which can broadcast the message
among connected clients.
'''

import socket, select


class chatServer(object):
	
	def __init__(self, port):
		self.host = ''
		self.port = port
		self.socket_list = []
		self.connected_list = []

	def setUpServer(self, socket):
		# create server socket waiting for the connection
		server_sock = socket.socket()
		server_sock.bind((self.host, self.port))
		server_sock.listen(1)
		self.socket_list.append(server_sock)
		print "Server starts from port " + str(self.port)
		print "waiting for a connection ..."

		while True:
			''' 
			Select() method can select sockets from the pool when the socket is ready.
			Socket_list stores all the readable sockets.
			Connected_list stores all the writable sockets, in our case,
			it is always empty, because we want the client can receive data
			after the connection instead of sending data to the server.
			'''
			ready_2_read, ready_2_send, in_error = select.select(self.socket_list, 
																 self.connected_list,
																 [])

			for socket in ready_2_read:
				
				# case 1, a server socket is ready for a connection
				if socket == server_sock:
					connection, client_address = socket.accept()
					print "new connection from " + str(client_address)
					# add the client socket to readable list for sending the data
					self.socket_list.append(connection)
					message = "[ %s ] entered our chat room.\n" % str(client_address)
					self.broadcast(server_sock, connection, message)
				
				# case 2, receive data from the client
				else:
					data = socket.recv(1024)
					if data:
						message = " [ " + str(socket.getpeername()) + " ] " + data
						self.broadcast(server_sock, socket, message)
					else:
						print "closing " + str(socket.getpeername()) + " after reading no data\n"
						self.socket_list.remove(socket)
						message = "[ %s ] is offline\n" % str(socket.getpeername())
						self.broadcast(server_sock, socket, message)
	

	def broadcast(self, server, client, message):
		for socket in self.socket_list:
			if socket != server and socket != client:
				try:
					socket.send(message)
				except:
					# bad connection
					socket.close()
					if socket in self.socket_list:
						self.socket_list.remove(socket)

if __name__ == '__main__':
	myServer = chatServer(8888)
	myServer.setUpServer(socket)