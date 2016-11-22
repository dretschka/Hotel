# assignment 4 task 1
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import socket
import sys
from urllib.parse import urlparse

#Get the command line argument
def get_url():
    args = sys.argv[1]
    #args = 'http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg'
    #args = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
    return args


#Parse the url in its components,
#create a socket and connect to a webserver on port 80.
#Send a GET Request and wait till all chunks arrived. If the next chunk is empty, continue.
def get_data(url):
    url_comps = urlparse(url)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url_comps.netloc, 80))
    sock.sendall(b'GET ' + bytes(url_comps.path, encoding='utf-8') + b' HTTP/1.0')
    sock.sendall(b'Host: ' + bytes(url_comps.netloc, encoding='utf-8'))
    sock.sendall(b'\n\n')
    data = b""
    while True:
        chunk = sock.recv(4096)
        data += chunk
        if not chunk:
            break
        del chunk
    return data

#Seperate the header from the content
def sep_data(data):
    i = data.find(b'\r\n\r\n')
    if i != -1:
        return data[:i], data[i:].strip()
    else:
        print('No Header found :(')
    return

#Determine the Content-Type
def get_contenttype(header):
    pos = header.decode().find("Content-Type:")
    if pos != -1:
        #Find "Content-Type"
        #Remove "Content-Type: " from selection
        c_type = header[pos+14:]
        i = c_type.find(b";")
        if i != -1:
            return c_type[:i]
        else:
            return c_type
    else:
        print('No content type found :(')
        return

#Write the header and content in files.
#If the content is an image, safe it with the correct name and file extension.
def write_file(header, content, url):
    headerfile = open('index.php.header', 'wb')
    headerfile.write(header)
    headerfile.close()

    if get_contenttype(header) == b"text/html":
        contentfile = open('index.php', 'wb')
        contentfile.write(content)
        contentfile.close()
    elif b"image" in get_contenttype(header):
        url_comps = urlparse(url)
        i = url_comps.path.rfind('/')
        print('\n')
        contentfile = open(url_comps.path[i+1:], 'wb')
        contentfile.write(content)
        contentfile.close()
    return

#call all functions
def main_func(url):
    data = get_data(url)
    header, content = sep_data(data)
    write_file(header, content, url)
    print(header.decode())


if __name__ == '__main__':
    main_func(get_url())
