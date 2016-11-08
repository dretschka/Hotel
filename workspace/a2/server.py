import socket
import json

s = socket.socket()
s.bind(('localhost', 8080))

s.listen(5)

while True:
	c, addr = s.accept()
	jsonData = c.recv(1024)
	jsonObj = json.loads(jsonData.decode())
	print('Name: ', jsonObj['Name'])
	print('Age: ', jsonObj['Age'])
	print('Matrikelnummer: ', jsonObj['Matrikelnummer'])
	c.close()