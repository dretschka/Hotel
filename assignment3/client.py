# assignment 3 task2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kircher - jkircher@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import socket
import json

s = socket.socket()
s.connect(('localhost', 8080))

url = input('Please insert url: ')

jsonObj = {'url': url}
jsonStr = json.dumps(jsonObj)

s.send(jsonStr.encode())

s.close()