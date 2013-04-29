import socket
import sys

CHUNK_SIZE = 4096

def run_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)

    print "Server listening on port %d" % port

    while True:
        client, addr = sock.accept()
        print "Got connection from %s" % addr[0]
        req = client.recv(CHUNK_SIZE)
        while req:
            client.send(req)
            req = client.recv(CHUNK_SIZE)
        client.close()
    sock.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    run_server(port)
