# assignment 3 task2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kircher - jkircher@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import socket
import json

s = socket.socket()
s.bind(('localhost', 8080))

s.listen(5)

while True:
	c, addr = s.accept()
	jsonData = c.recv(1024)
	jsonObj = json.loads(jsonData.decode())
	print('Protocol: ')
	print('Domiain: ')
	print('Sub-Domain: ')
	print('Port Number: ')
	print('Path: ')
	print('Parameters: ')
	print('Fragment: ')
	c.close()