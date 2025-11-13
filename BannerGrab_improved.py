import socket
Ports = [21,22,25,3306]
for i in range (0,4):
	s = socket.socket()
	Port = Ports[i]
	print("This is the banner for the port")
	print(Port)
	s.connect(("192.168.1.101", Port))
	answer=s.recv(1024)
	print(answer)
	s.close()