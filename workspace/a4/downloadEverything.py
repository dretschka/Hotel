# assignment 4 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import sys
import re
import client
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

    for i in range(0, len(links)):
        url_comps = urlparse(links[i][0])
        if url_comps.netloc == "":
            links[i] = domain.scheme + "://" + domain.netloc + links[i][0]
        else:
            links[i] = links[i][0]
    return links


def download_images(links):
    for i in range(0, len(links)):
        print('\n ' + str(i) + '\n')
        client.main_func(links[i])

data = get_file('index.php')
links = get_urls(data)
download_images(links)
print(links)
