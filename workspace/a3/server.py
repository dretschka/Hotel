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
	
	# find protocol
	prot = 'standard assumed: http'
	protPos = urlString.find("://")
	if protPos != -1:
		prot = urlString[:protPos]
	else:
		protPos = -3
		
	# determine domains and port
	port = 'standard port assumed: 80'
	portPos = urlString.find(":", protPos+1)
	pathPos = urlString.find("/", protPos+3)
	if portPos != -1:
		domain = urlString[protPos+3: portPos]
		port = urlString[portPos+1: pathPos]
	else:
		if pathPos != -1:
			domain = urlString[protPos+3: pathPos]
		else:	
			domain = urlString[protPos+3:]
	subdomain = 'none'
	lastDot = domain.rfind(".")
	subdomaintmp = domain[:lastDot]	
	subDot = subdomaintmp.rfind(".")
	if subDot != -1:
		subdomain = subdomaintmp[:subDot]	
	
	# find path ?
	valPos = urlString.find("?")
	path = 'none given'
	if pathPos != -1:
		path = urlString[pathPos+1:valPos]
	
	# find value
	fragPos = urlString.find("#")
	val = 'none given'
	if valPos != -1:
		val = urlString[valPos+1: fragPos]
		
	# determine fragment
	frag = 'no fragment'
	if fragPos != -1:
		frag = urlString[fragPos+1:]
	
	
	print('Url: ', jsonObj['url'])
	print('Protocol: ', prot)
	print('Domiain: ', domain)
	print('Sub-Domain: ', subdomain)
	print('Port Number: ', port)
	print('Path: ', path)
	print('Parameters: ', val)
	print('Fragment: ', frag)
	
	c.close()
	
# test url	
# http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument	