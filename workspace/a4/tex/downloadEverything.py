# assignment 4 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de


import sys
import re
import client
from urllib.parse import urlparse

#Parse filename and url
def get_args():
    filename = sys.argv[1]
    url = sys.argv[2]
    return filename, url

#open the file
def get_file(filename):
    file = open(filename, 'br')
    return file.read()

#Get all image urls from the file
def get_urls(data, url):
    domain = urlparse(url)
    pattern = re.compile("<img.+?src=[\"'](.+?)[\"'].*?>")
    images = pattern.findall(data.decode())

    #Fix relative paths
    for i in range(0, len(images)):
        url_comps = urlparse(images[i])
        if url_comps.netloc == "":
            images[i] = domain.scheme + "://" + domain.netloc + images[i]
        else:
            images[i] = images[i]
    return images


#iterate over the list and call the function from task 01
def download_images(links):
    for i in range(0, len(links)):
        print('\n ' + str(i) + '\n')
        client.main_func(links[i])

#call all functions
def main_func():
    filename, url = get_args()
    data = get_file(filename)
    links = get_urls(data, url)
    download_images(links)
#    print(links)


if __name__ == '__main__':
    main_func()