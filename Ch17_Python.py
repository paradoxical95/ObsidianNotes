#Banner Grabbing script
import socket
s = socket.socket()
""" a variable, that stores the socket() method from the class socket so we can reference this variable instead 
of writing socket.socket().connect() everytime"""
s.connect(("192.168.1.101", 22))
"""after connecting to a machine on your network who has Port 22 open for SSH, 
we try to use the recv() fn to grab 1024 bytes of data, which will contain the banner info."""
answer = s.recv(1024)
print(answer)
s.close
# running this by entering the other machine's IP will fetch a result like
# "SSH-2.0-OPENSSH_7.3p1 Debian-1"
# This is what shodan.io does in essence.