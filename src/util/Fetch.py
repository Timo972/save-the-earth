# import urllib2
# 
# def fetchUrl(url):
#     print("fetch url {}".format(url))
#     urlrequest = urllib2.Request(url)
#     print("prepared request")
#     responseStr = urllib2.urlopen(urlrequest)
#     print("got response")
#     return responseStr

import socket
import ssl

def fetchUrl(host, port, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s = ssl.wrap_socket(s)
    request = "GET {1} HTTP/1.1\r\nHost: {0} \r\n\r\n".format(host, path)
    s.sendall(request)
    reply = s.recv(4096)
    print("got url reply {}".format(reply))
    return reply