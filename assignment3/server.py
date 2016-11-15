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
	
	urlString = jsonObj['url']
	
	urlSplitList = urlString.split("://")
	
	print('Url: ', jsonObj['url'])
	print('Protocol: ', urlSplitList[0])
	print('Domiain: ')
	print('Sub-Domain: ')
	print('Port Number: ')
	print('Path: ')
	print('Parameters: ')
	print('Fragment: ')
	
	print(urlSplitList)
	c.close()
	
	
# http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument	