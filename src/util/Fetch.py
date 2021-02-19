import urllib2

def fetchUrl(url):
    print("fetch url {}".format(url))
    urlrequest = urllib2.Request(url)
    print("prepared request")

    try:
        responseStr = urllib2.urlopen(urlrequest)
    except urllib2.HTTPError as e:
        print("------ERROR------")
        print("HTTPError")
        print(e)
        print("-----------------")
        return None
    except urllib2.URLError as e:
        print("------ERROR------")
        print("URLError")
        print(e)
        print("-----------------")
        return None
    except:
        print("------ERROR------")
        print("unknown fetch error")
        print("-----------------")
        return None

    print("got response")
    return responseStr

# import socket
# import ssl
# 
# def fetchUrl(host, port, path):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((host, port))
#     s = ssl.wrap_socket(s)
#     request = "GET {1} HTTP/1.1\r\nHost: {0} \r\n\r\n".format(host, path)
#     s.sendall(request)
#     reply = s.recv(4096)
#     print("got url reply {}".format(reply))
#     return reply