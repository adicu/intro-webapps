import socket
import sys
import os

CHUNK_SIZE = 4096

EXT2MIME = {'.html' : 'text/html',
            '.txt'  : 'text/plain',
            '.js'   : 'text/javascript',
            '.css'  : 'text/css'}

def serve_page(client):
    req = ''

    while '\r\n\r\n' not in req and '\n\n' not in req:
        req += client.recv(CHUNK_SIZE)

    topline = req.split('\n')[0]
    topline = topline.strip()
    url = topline.split(' ')[1]
    fname = os.path.join(os.getcwd(), url[1:])
    _, ext = os.path.splitext(fname)
    mime = EXT2MIME.get(ext, 'application/octet-stream')

    if os.path.isfile(fname):
        f = open(fname)
        length = os.path.getsize(fname)
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: " + mime + "\r\n")
        client.send("Content-Length: " + str(length) + "\r\n\r\n")

        for line in f:
            client.send(line)
    else:
        client.send("HTTP/1.1 404 Not Found\r\n\r\n")

def run_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)

    print "Server listening on port %d" % port
    
    try:
        while True:
            client, addr = sock.accept()
            print "Got connection from %s" % addr[0]
            serve_page(client)
            client.close()
    except KeyboardInterrupt:
        print "Got Ctrl-C, exiting"
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run_server(port)
