import sys
import re

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
    return links

data = get_file('index.php')
links = get_urls(data)
print(links)
print(len(links))

