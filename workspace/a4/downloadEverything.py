# assignment 4 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import sys
import re
from urllib.parse import urlparse
domain = urlparse('http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science')

#Recieve filename and url
def get_args():
    #args = sys.argv[1]
    #print(args)
    #args = 'http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg'
    args = 'http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science'
    return args


def get_file(filename):
    file = open(filename, 'br')
    return file.read()


def get_urls(data):
    pattern = re.compile('(<img .* \/>)')
    images = pattern.findall(data.decode())

    pattern2 = re.compile('(?<=src=")(.*?)(?=")')
    links = []
    for element in images:
        links.append(pattern2.findall(element))

    for i in range(0,len(links)):
        url_comps = urlparse(links[i][0])
        if url_comps.netloc == "":
            links[i] = domain.scheme + "://" + domain.netloc + links[i][0]
        else:
            links[i] = links[i][0]
    return links

def download_images(links):
    for i in range(0, len(links)):
         links[i]

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


def sep_data(data):
    i = data.find(b'\r\n\r\n')
    if i != -1:
        return data[:i], data[i:].strip()
    else:
        print('No Header found :(')
    return


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


def write_file(header, content):
    headerfile = open('index.php.header', 'wb')
    headerfile.write(header)
    headerfile.close()

    if get_contenttype(header) == b"text/html":
        contentfile = open('index.php', 'wb')
        contentfile.write(content)
        contentfile.close()
    elif get_contenttype(header) == b"image/jpeg":
        url_comps = urlparse(get_url())
        i = url_comps.path.rfind('/')
        contentfile = open(url_comps.path[i+1:], 'wb')
        contentfile.write(content)
        contentfile.close()
    return


data = get_file('index.php')
links = get_urls(data)
print(links)
print(domain)