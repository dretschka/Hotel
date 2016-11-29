# assignment 5 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

# HTTP Requests
import socket

# Parse the URLs und decode them
import urllib.parse

# Required for the makedirs command which is used to create the folder structure
import os

# Required for regular expressions
import re

# Used for time-measuring (debug purposes)
import time

# Globals
visited = set()
set_queue = set()
ext_links = 0
downloaded = 0
total_links = []


def recv_all(sock):
    data = b""
    part = None
    while part != b"":
        part = sock.recv(4096)
        data += part
    return data


# Parse the url in its components,
# create a socket and connect to a webserver on port 80.
# Send a GET Request and wait till all chunks arrived.
# If the next chunk is empty, continue.
def do_http_get_request(url):
    url = urllib.parse.urlparse(url)
    path = url.path
    if path == "":
        path = "/"
    host = url.netloc
    port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    request = ""
    request += "GET " + path + " HTTP/1.0"
    request += "\r\n\r\n"

    s.send(str.encode(request))
    response = recv_all(s)

    if response:
        temp = response.split(b"\r\n\r\n", 1)
        header = temp[0]
        body = temp[1].strip()

        return header, body, path
    else:
        print("No response :(")
        exit()


def save_to_file(body, path):
    global downloaded
    # remove first / in order to save the file in the directory of this .py file
    if path[0:1] == "/":
        path = path[1:]

    # convert path to UTF-8
    path = urllib.parse.unquote_plus(path)

    # create directories if not already exist
    if path.count("/") > 0:
        os.makedirs(os.path.dirname("dump/" + path), exist_ok=True)

    file = open("dump/" + path, 'wb')
    file.write(body)
    file.close()
    downloaded += 1


def search_all_links(body, url):
    global ext_links, visited, set_queue, total_links
    q = set()
    count_external_links = 0
    count_internal_links = 0

    url = urllib.parse.urlparse(url)
    pattern = re.compile("<a.+?href=[\"'](.+?)[\"'].*?>")

    # Sometimes there is an Unicode Decode Error, so we simply catch it, log it and proceed
    try:
        links = pattern.findall(body.decode())
    except UnicodeDecodeError as ude:
        return -1

    # Do stuff with all found links
    for i in range(0, len(links)):
        url_i = urllib.parse.urlparse(links[i])

        # Ignore external links
        if url_i.netloc != '':
            if url_i.netloc != '141.26.208.82':
                # Count all external links
                count_external_links += 1
                continue
            else:
                break

        # Count all internal links
        count_internal_links += 1
        count = links[i].count("../")

        # Remove all ../ from the URL
        for j in range(0, count):
            index = links[i].find("/")
            links[i] = links[i][index+1:]

        temp_path = url.path
        # count+1 because we have to remove the filename first :)
        for y in range(0, count+1):
            x = temp_path.rfind('/')
            temp_path = temp_path[:x]

        # If the path has a leading / remove it
        if temp_path[0:1] == "/":
            temp_path = temp_path[1:]

        result = url.scheme + "://" + url.netloc + "/" + temp_path + links[i]

        # # Check if URL is already visited
        if result in visited or result in set_queue:
            continue

        q.add(result)

    total_links.append((count_internal_links + count_external_links, count_internal_links, count_external_links))
    return q


def print_log(duration, decoding_error):
    duration_min = str(round(duration/60, 1)) + " min."
    duration_perc = "(" + str(round(((duration/1645)*100), 2)) + "%)"
    downloaded_perc = "(" + str(round(((downloaded/85322)*100), 1)) + "%)"
    file = open('log.txt', 'a')
    file.write("Duration: %-9s %-9s | Visited: %-8s | Queue: %-8s | Decoding-Errors: %-2s | Downloaded: %-5s %-7s\n" %
               (duration_min, duration_perc, len(visited), len(set_queue), decoding_error, downloaded, downloaded_perc))
    file.close()


def worker(starting_url):
    global visited, set_queue
    start_time = time.time()
    set_queue.add(starting_url)
    decoding_error = 0

    c = 0

    while len(set_queue) > 0:
        c += 1

        # Logging
        if c % 1000 == 0:
            t = (time.time() - start_time)
            print_log(t, decoding_error)

        current_url = set_queue.pop()

        visited.add(current_url)

        # Download current file
        header, response, path = do_http_get_request(current_url)

        if header.count(b"200 OK") == 0:
            continue

        save_to_file(response, path)

        # If Unicode Error, log and continue
        link_set = search_all_links(response, current_url)
        if link_set != -1:
            set_queue.symmetric_difference_update(link_set)
        else:
            decoding_error += 1
            file = open('log.txt', 'a')
            file.write("\n ********** UTF8 DECODING ERROR ********** \n\n")
            file.write("\n\n BTW: Found %s links until now \n\n" % len(total_links))
            file.close()
            continue

    t = (time.time() - start_time)
    print_log(t, decoding_error)
    file = open('log.txt', 'a')
    file.write("\n *************************************** \n")
    file.write("\n\n ********** FINISHED CRAWLING ********** \n\n")
    file.write("\n *************************************** \n")
    file.close()

    return


# returns all necessary information for task 3
def report_func():
    # Total amount of webpages
    # external and internal links per webbpage
    main_func()

    # total links: [(total links, internal links, external links)]
    return visited, total_links


# call all functions
def main_func():
    # Create download folder
    os.makedirs(os.path.dirname("dump/"), exist_ok=True)

    # Create a new file or overwrite the existing one
    file = open('log.txt', 'w')
    file.write("Start crawling ... \n")
    file.close()
    url = 'http://141.26.208.82/articles/g/e/r/Germany.html'
    worker(url)


if __name__ == '__main__':
    main_func()
