import socket
import json

s = socket.socket()
s.connect(('localhost', 8080))

name = input('Please insert name: ')
age = input('Please insert age: ')
mat = input('Please insert matrikelnumber: ')

jsonObj = {'Name': name, 'Age': age, 'Matrikelnummer': mat}
jsonStr = json.dumps(jsonObj)

s.send(jsonStr.encode())

s.close()