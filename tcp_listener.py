import socket

TCP_IP = ""
TCP_PORT = 6996
BUFFER_SIZE = 100

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print("Connection Address : ",addr)

while 1:
		data=conn.recv(BUFFER_SIZE)
		if not data:
			break
		print("Received Data : ", data)
		conn.send(data)

conn.close()